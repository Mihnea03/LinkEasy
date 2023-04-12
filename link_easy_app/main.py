from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import validators
import string
from random import choices
from sqlalchemy.orm import Session

from . import schemas, models
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

# def raise_not_found(request):

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid!")
    
    key = "".join(choices(string.ascii_uppercase, k=5))
    secret_key = "".join(choices(string.ascii_uppercase, k=8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    db.add(db_url)
    db.commit()

    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url
