from pydantic import BaseModel

class File(BaseModel):
    user_token : int
    month : int
    year : int
    upload_date : str
    descr_file : str