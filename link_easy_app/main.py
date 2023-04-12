from fastapi import FastAPI, HTTPException
from validators import url

from . import schemas

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url")
def create_url(url: schemas.URLBase):
    if not url(url.target_url):
        raise_bad_request("Your provided URL is not valid!")
    return f"TODO: Create database entry for: {url.target_url}"