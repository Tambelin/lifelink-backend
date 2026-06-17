from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String(100))

    blood_group = Column(String(10))

    city = Column(String(100))

    hospital = Column(String(150))

    units_needed = Column(Integer)

    contact_phone = Column(String(30))

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )