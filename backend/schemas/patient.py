from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    location: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
