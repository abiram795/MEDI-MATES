from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from backend.utils.supabase_client import get_current_user, CurrentUser, supabase_admin, require_role

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])

@router.get("/")
def get_doctors(
    search: Optional[str] = None,
    specialty_id: Optional[str] = None,
    hospital_id: Optional[str] = None
):
    # Query hospital_doctors to get relationships
    query = supabase_admin.table('hospital_doctors').select('*, doctors(*, specialties(*)), hospitals(hospital_name, address, id)')

    if hospital_id:
        query = query.eq('hospital_id', hospital_id)

    res = query.execute()

    # Filter in Python if Supabase filtering on related tables gets too complex
    results = []
    for record in res.data:
        doc = record.get('doctors')
        if not doc:
            continue

        if search and search.lower() not in doc.get('name', '').lower():
            continue

        if specialty_id and doc.get('specialty_id') != specialty_id:
            continue

        # Combine the relation info
        doc_info = {**doc}
        doc_info['hospital'] = record.get('hospitals')
        doc_info['availability_info'] = record.get('availability_info')
        doc_info['contact_info'] = record.get('contact_info')
        results.append(doc_info)

    return results

@router.get("/{doctor_id}")
def get_doctor(doctor_id: str):
    res = supabase_admin.table('doctors').select('*, specialties(*), hospital_doctors(availability_info, hospitals(hospital_name, address))').eq('id', doctor_id).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return res.data[0]

@router.get("/specialties/all")
def get_specialties():
    res = supabase_admin.table('specialties').select('*').order('name').execute()
    return res.data
