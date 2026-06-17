from fastapi import APIRouter, Depends

from app.auth_dependencies import get_current_user
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user