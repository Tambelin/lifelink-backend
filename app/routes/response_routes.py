from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.response_models import RequestResponse
from app.request_models import BloodRequest
from app.notification_models import Notification
from app.auth_dependencies import get_current_user
from app.models import User

router = APIRouter(
    prefix="/responses",
    tags=["Responses"]
)


@router.post("/{request_id}")
def respond_to_request(
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
            detail="Blood request not found"
        )

    existing_response = (
        db.query(RequestResponse)
        .filter(
            RequestResponse.request_id == request_id,
            RequestResponse.donor_id == current_user.id
        )
        .first()
    )

    if existing_response:
        raise HTTPException(
            status_code=400,
            detail="You have already volunteered for this request"
        )

    response = RequestResponse(
        request_id=request_id,
        donor_id=current_user.id
    )

    db.add(response)

    notification = Notification(
        user_id=request.owner_id,
        message=f"{current_user.full_name} volunteered to donate blood for {request.patient_name}"
    )

    db.add(notification)

    db.commit()

    return {
        "message": "Response submitted successfully"
    }


@router.get("/request/{request_id}")
def get_request_responses(
    request_id: int,
    db: Session = Depends(get_db)
):
    responses = (
        db.query(RequestResponse)
        .filter(
            RequestResponse.request_id == request_id
        )
        .all()
    )

    result = []

    for response in responses:
        donor = (
            db.query(User)
            .filter(User.id == response.donor_id)
            .first()
        )

        if donor:
            result.append({
                "id": donor.id,
                "full_name": donor.full_name,
                "email": donor.email,
                "blood_group": donor.blood_group,
                "city": donor.city
            })

    return result