from pydantic import BaseModel

class Medicine(BaseModel):
    descr_medicine : str
    id_type : str
    unit_value : float
    month : int
    year : int