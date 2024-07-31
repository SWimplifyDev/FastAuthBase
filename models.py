from pydantic import BaseModel


class User(BaseModel):
    full_name: str
    email: str


class UserInDB(User):
    password: str
    disabled: bool = False
