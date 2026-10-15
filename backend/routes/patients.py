from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.utils.supabase_client import get_current_user, CurrentUser, supabase_admin, require_role

router = APIRouter(prefix="/api/patients", tags=["Patients"])

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None

@router.get("/me")
def get_patient_profile(current_user: CurrentUser = Depends(require_role("patient"))):
    res = supabase_admin.table('patients').select('*').eq('id', current_user.id).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return res.data[0]

@router.put("/me")
def update_patient_profile(profile_data: PatientUpdate, current_user: CurrentUser = Depends(require_role("patient"))):
    update_data = profile_data.dict(exclude_unset=True)
    if not update_data:
        return get_patient_profile(current_user)

    res = supabase_admin.table('patients').update(update_data).eq('id', current_user.id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Failed to update patient profile")
    return res.data[0]
