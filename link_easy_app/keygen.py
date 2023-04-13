import string
import random

KEY_LENGTH = 5
ADMIN_KEY_LENGTH = 8

def create_key(len: int) -> str:
    data_choice = string.ascii_uppercase + string.digits
    return "".join(random.choices(data_choice, k=len))
