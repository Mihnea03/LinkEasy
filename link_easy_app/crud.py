from sqlalchemy.orm import Session

from . import schemas, models
from keygen import KEY_LENGTH, ADMIN_KEY_LENGTH, create_key

def create_db_url (db: Session, url:schemas.URLBase) -> models.URL:
    key = create_key(KEY_LENGTH)
    secret_key = create_key(ADMIN_KEY_LENGTH)

    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url