from pydantic import BaseModel

class Control(BaseModel):
    id_medicine : int
    unit_quantity : float
    total_value : float
    month : int
    year : int
    id_origin : int
    id_destination : int
    id_upload_file : int