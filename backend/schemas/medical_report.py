from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MedicalReportBase(BaseModel):
    file_name: str
    report_type: Optional[str] = None

class MedicalReportResponse(MedicalReportBase):
    id: int
    patient_id: int
    uploaded_at: datetime
    analysis_status: str
    summary: Optional[str] = None
    observations: Optional[List[Dict[str, Any]]] = None
    out_of_range_values: Optional[List[Dict[str, Any]]] = None
    simple_explanation_en: Optional[str] = None
    simple_explanation_ta: Optional[str] = None
    questions_for_doctor: Optional[List[str]] = None
    follow_up_notes: Optional[List[str]] = None

    class Config:
        from_attributes = True
