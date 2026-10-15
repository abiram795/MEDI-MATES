from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.utils.supabase_client import supabase_admin, supabase_anon

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class AuthLogin(BaseModel):
    email: str
    password: str

class AuthRegister(BaseModel):
    email: str
    password: str
    role: str

@router.post("/register")
def register_user(user: AuthRegister):
    if user.role.lower() not in ["patient", "hospital"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be PATIENT or HOSPITAL")

    # Use admin client to create user to bypass restrictions if needed, or anon
    res = supabase_anon.auth.sign_up({
        "email": user.email,
        "password": user.password
    })

    if res.user is None:
        raise HTTPException(status_code=400, detail="Registration failed. Email might be in use.")

    # Supabase triggers might create the profile automatically, but let's ensure it's there
    try:
        # Assuming the profile is created by a trigger, we just update the role.
        # If trigger doesn't exist, this will insert
        supabase_admin.table('profiles').upsert({
            'id': res.user.id,
            'email': user.email,
            'role': user.role.lower()
        }).execute()

        # Also create empty patient/hospital record based on role
        if user.role.lower() == "patient":
            supabase_admin.table('patients').insert({
                'id': res.user.id,
                'full_name': user.email.split('@')[0]
            }).execute()
        elif user.role.lower() == "hospital":
            supabase_admin.table('hospitals').insert({
                'id': res.user.id,
                'hospital_name': user.email.split('@')[0]
            }).execute()

    except Exception as e:
        print("Error setting up profile:", e)
        pass # Not blocking if trigger handles it

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user_data: AuthLogin):
    try:
        res = supabase_anon.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })

        if not res.session:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        user_id = res.user.id

        # Fetch role from profiles
        profile_res = supabase_admin.table('profiles').select('role').eq('id', user_id).limit(1).execute()
        role = profile_res.data[0]['role'].upper() if profile_res.data else "PATIENT"

        return {
            "access_token": res.session.access_token,
            "token_type": "bearer",
            "role": role
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")
