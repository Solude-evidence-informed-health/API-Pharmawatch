from pydantic import BaseModel

class File(BaseModel):
    user_token: int
    upload_date: str