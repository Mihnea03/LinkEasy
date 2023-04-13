from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import validators
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, SessionLocal
from .keygen import create_key
from .crud import create_db_url, get_db_url_by_key

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist!"
    raise HTTPException(status_code=404, detail=message)

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid!")
    
    db_url = create_db_url(db, url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    return db_url

@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    db_url = get_db_url_by_key(url_key=url_key)
    if db_url:
        return RedirectResponse(url=db_url.target_url)
    else:
        raise_not_found(request)

