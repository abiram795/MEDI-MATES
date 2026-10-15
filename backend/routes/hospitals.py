from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from backend.utils.supabase_client import get_current_user, CurrentUser, supabase_admin, require_role

router = APIRouter(prefix="/api/hospitals", tags=["Hospitals"])

@router.get("/")
def get_hospitals(search: Optional[str] = None):
    query = supabase_admin.table('hospitals').select('*, hospital_locations(*)').eq('approved', True)
    if search:
        query = query.ilike('hospital_name', f"%{search}%")
    res = query.execute()
    return res.data

@router.get("/me")
def get_hospital_profile(current_user: CurrentUser = Depends(require_role("hospital"))):
    res = supabase_admin.table('hospitals').select('*, hospital_locations(*)').eq('id', current_user.id).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Hospital profile not found")
    return res.data[0]

@router.put("/me")
def update_hospital_profile(hospital_data: dict, current_user: CurrentUser = Depends(require_role("hospital"))):
    # Split into hospital and location data if needed, simplified for now
    update_data = {k: v for k, v in hospital_data.items() if k in ['hospital_name', 'phone', 'address', 'hospital_type', 'website_url', 'appointment_url', 'hospital_image_url']}
    if update_data:
        supabase_admin.table('hospitals').update(update_data).eq('id', current_user.id).execute()

    # Simple location update logic (assuming hospital_data has latitude, longitude)
    if 'latitude' in hospital_data and 'longitude' in hospital_data:
        loc_data = {
            'hospital_id': current_user.id,
            'latitude': hospital_data['latitude'],
            'longitude': hospital_data['longitude']
        }
        supabase_admin.table('hospital_locations').upsert(loc_data).execute()

    return get_hospital_profile(current_user)

@router.get("/{hospital_id}")
def get_hospital(hospital_id: str):
    res = supabase_admin.table('hospitals').select('*, hospital_locations(*), hospital_doctors(doctors(*, specialties(*)))').eq('id', hospital_id).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return res.data[0]
