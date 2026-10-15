from fastapi import APIRouter, Depends, HTTPException
from backend.utils.supabase_client import get_current_user, CurrentUser, supabase_admin, require_role

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/users")
def get_all_users(current_user: CurrentUser = Depends(require_role("admin"))):
    res = supabase_admin.table('profiles').select('*').execute()
    return res.data

@router.get("/hospitals")
def get_all_hospitals(current_user: CurrentUser = Depends(require_role("admin"))):
    res = supabase_admin.table('hospitals').select('*').execute()
    return res.data

@router.get("/doctors")
def get_all_doctors(current_user: CurrentUser = Depends(require_role("admin"))):
    res = supabase_admin.table('doctors').select('*').execute()
    return res.data

@router.put("/hospitals/{hospital_id}/approve")
def approve_hospital(hospital_id: str, current_user: CurrentUser = Depends(require_role("admin"))):
    res = supabase_admin.table('hospitals').update({'approved': True}).eq('id', hospital_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"message": "Hospital approved successfully"}

@router.put("/hospitals/{hospital_id}/reject")
def reject_hospital(hospital_id: str, current_user: CurrentUser = Depends(require_role("admin"))):
    res = supabase_admin.table('hospitals').update({'approved': False}).eq('id', hospital_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"message": "Hospital rejected successfully"}
