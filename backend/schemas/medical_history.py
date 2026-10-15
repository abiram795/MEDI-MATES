from pydantic import BaseModel
from typing import Optional
from datetime import date

class MedicalHistoryBase(BaseModel):
    condition: str
    date: date
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    notes: Optional[str] = None
    treatment: Optional[str] = None
    status: Optional[str] = None

class MedicalHistoryCreate(MedicalHistoryBase):
    pass

class MedicalHistoryUpdate(MedicalHistoryBase):
    pass

class MedicalHistoryResponse(MedicalHistoryBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True
