from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.request_models import BloodRequest
from app.schemas import BloodRequestCreate
from app.auth_dependencies import get_current_user
from app.models import User

router = APIRouter(
    prefix="/requests",
    tags=["Requests"]
)


@router.post("/")
def create_request(
    request: BloodRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_request = BloodRequest(
        patient_name=request.patient_name,
        blood_group=request.blood_group,
        city=request.city,
        hospital=request.hospital,
        units_needed=request.units_needed,
        contact_phone=request.contact_phone,
        owner_id=current_user.id,
        status="ACTIVE"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "message": "Blood request created successfully"
    }


@router.get("/")
def get_requests(
    db: Session = Depends(get_db)
):
    requests = (
        db.query(BloodRequest)
        .filter(BloodRequest.status == "ACTIVE")
        .all()
    )

    return requests


@router.get("/my")
def get_my_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    requests = (
        db.query(BloodRequest)
        .filter(
            BloodRequest.owner_id == current_user.id
        )
        .all()
    )

    return requests


@router.patch("/{request_id}/fulfill")
def fulfill_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    request = (
        db.query(BloodRequest)
        .filter(BloodRequest.id == request_id)
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    if request.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    request.status = "FULFILLED"

    db.commit()

    return {
        "message": "Request marked as fulfilled"
    }


@router.delete("/{request_id}")
def delete_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    request = (
        db.query(BloodRequest)
        .filter(BloodRequest.id == request_id)
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    if request.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(request)
    db.commit()

    return {
        "message": "Request deleted successfully"
    }