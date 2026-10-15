from pydantic import BaseModel
from typing import Optional

class DoctorBase(BaseModel):
    name: str
    specialization: str
    qualifications: Optional[str] = None
    experience_years: Optional[int] = None
    languages: Optional[str] = None
    availability: Optional[str] = None
    about: Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    hospital_id: int
    is_approved: bool

    class Config:
        from_attributes = True
