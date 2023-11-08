from pydantic import BaseModel

class User(BaseModel):
    token: str
    first_name: str
    last_name: str
    organization: int
    email: str

