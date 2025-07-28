from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, get_current_admin_user
from app.models.models import User

router = APIRouter()

@router.get("/profile")
def read_profile(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}

@router.get("/admin/dashboard")
def read_admin_dashboard(current_admin: User = Depends(get_current_admin_user)):
    return {"message": f"Welcome Admin {current_admin.email}"}
