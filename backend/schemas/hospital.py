from pydantic import BaseModel
from typing import Optional, List

class HospitalServiceBase(BaseModel):
    name: str
    description: Optional[str] = None

class HospitalServiceResponse(HospitalServiceBase):
    id: int
    hospital_id: int

    class Config:
        from_attributes = True

class HospitalBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdate(HospitalBase):
    pass

class HospitalResponse(HospitalBase):
    id: int
    user_id: int
    is_approved: bool

    class Config:
        from_attributes = True
