from supabase import create_client, Client
from backend.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

supabase_admin: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
supabase_anon: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class CurrentUser(BaseModel):
    id: str
    email: str
    role: str

def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    try:
        # Verify JWT with Supabase using the anon client
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = user_response.user.id
        email = user_response.user.email

        # Fetch profile role
        profile_res = supabase_admin.table('profiles').select('role').eq('id', user_id).limit(1).execute()
        role = profile_res.data[0]['role'] if profile_res.data else "patient" # default

        return CurrentUser(id=user_id, email=email, role=role)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {str(e)}")

def require_role(required_role: str):
    def role_checker(current_user: CurrentUser = Depends(get_current_user)):
        if current_user.role.lower() != required_role.lower():
            raise HTTPException(status_code=403, detail="Not authorized for this role")
        return current_user
    return role_checker

def get_supabase_admin() -> Client:
    return supabase_admin
