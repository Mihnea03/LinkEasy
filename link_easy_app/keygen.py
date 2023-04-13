import string
import random
import crud
from sqlalchemy.orm import Session

KEY_LENGTH = 5
ADMIN_KEY_LENGTH = 8

def create_key(len: int) -> str:
    data_choice = string.ascii_uppercase + string.digits
    return "".join(random.choices(data_choice, k=len))

def create_unique_key(db: Session) -> str:
    key = create_key(KEY_LENGTH)

    while crud.get_db_url_by_key(db, key):
        key = create_key(KEY_LENGTH)
    
    return key