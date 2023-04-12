from sqlalchemy import String, Boolean, Integer, Column

from .database import Base

def URL(BASE):
    __tablename__ = "urls"

    id = Column(Integer, primary_key= True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)