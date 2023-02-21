from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    Id: int = None
    Username: str
    Password: str
    Fullname: str = None
    isAdmin: bool = None
