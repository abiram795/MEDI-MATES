from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicalDocumentBase(BaseModel):
    file_name: str
    document_type: Optional[str] = None

class MedicalDocumentResponse(MedicalDocumentBase):
    id: int
    patient_id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
