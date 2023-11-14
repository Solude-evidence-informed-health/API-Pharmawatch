from pydantic import BaseModel

class User(BaseModel):
    token : str
    descr_first_name : str
    descr_last_name : str
    organization : int
    descr_email : str

