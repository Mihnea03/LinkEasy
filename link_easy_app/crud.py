from sqlalchemy.orm import Session

from . import schemas, models
from keygen import KEY_LENGTH, ADMIN_KEY_LENGTH, create_unique_key, create_key

def get_db_url_by_key(db: Session, url_key:str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )

def create_db_url (db: Session, url:schemas.URLBase) -> models.URL:
    key = create_unique_key(db)
    secret_key = f"{key}_{create_key(ADMIN_KEY_LENGTH)}"

    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url