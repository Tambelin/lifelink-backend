from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class RequestResponse(Base):
    __tablename__ = "request_responses"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(
        Integer,
        ForeignKey("blood_requests.id")
    )

    donor_id = Column(
        Integer,
        ForeignKey("users.id")
    )