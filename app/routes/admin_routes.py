from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.request_models import BloodRequest
from app.response_models import RequestResponse
from app.notification_models import Notification

from app.admin_dependencies import (
    get_admin_user
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/stats")
def admin_stats(
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    return {
        "users": db.query(User).count(),
        "requests": db.query(BloodRequest).count(),
        "responses": db.query(RequestResponse).count(),
        "notifications": db.query(Notification).count()
    }