import string
import random

def create_key(len: int) -> str:
    data_choice = string.ascii_uppercase + string.digits
    return "".join(random.choices(data_choice, k=len))
