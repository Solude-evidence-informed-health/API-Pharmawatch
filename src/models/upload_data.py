from pydantic import BaseModel

class RawMedicineData(BaseModel):
    descr_medicine : str
    descr_unit_type : str
    unit_quantity : float
    unit_value : float
    total_value : float
    month : int
    year : int
    descr_origin : str
    descr_destination : str