from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import validators
from sqlalchemy.orm import Session

from . import schemas, models, crud
from .database import engine, SessionLocal

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
    
    db_url = crud.create_db_url(db, url)
    crud.set_db_url(db_url=db_url)
    return db_url

@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    db_url = crud.get_db_url_by_key(db=db, url_key=url_key)
    if db_url:
        crud.update_db_clicks(db, db_url)
        return RedirectResponse(url=db_url.target_url)
    else:
        raise_not_found(request)

@app.get(
    "/admin/{secret_key}",
    name="Administration Info",
    response_model=schemas.URLInfo)
def get_url_info(
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_secret_key(db= db, secret_key= secret_key):
        crud.set_db_url(db_url=db_url)
        return db_url
    else:
        raise_not_found(request)

@app.delete("/{secret_key}")
def delete_url(
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if db_url := crud.delete_db_url_by_secret_key(db, secret_key):
        message = f"Succesfully deleted shortened URL for: '{db_url.target_url}'"
        return { "detail": message }
    else:
        raise_not_found(request)