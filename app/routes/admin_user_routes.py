from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.admin_dependencies import get_admin_user

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"]
)


@router.get("/")
def get_all_users(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    return db.query(User).all()


@router.patch("/{user_id}/promote")
def promote_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_admin = True

    db.commit()

    return {
        "message": "User promoted to admin"
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }