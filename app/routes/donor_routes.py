from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

router = APIRouter(prefix="/donors")

@router.get("/")
def get_donors(
    blood_group: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if blood_group:
        query = query.filter(
            User.blood_group == blood_group
        )

    return [
    {
        "id": donor.id,
        "full_name": donor.full_name,
        "email": donor.email,
        "blood_group": donor.blood_group,
        "city": donor.city
    }
    for donor in query.all()
]