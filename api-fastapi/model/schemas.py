from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    Username: str
    Password: str
    Fullname: str
    isAdmin: bool
