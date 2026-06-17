from sqlalchemy import Column, String, Boolean
from app.database import Base
from app.notification_models import Notification
import uuid


class User(Base):

    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    full_name = Column(String(100))
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    blood_group = Column(String(5))
    city = Column(String(100))
    
    is_admin = Column(Boolean, default=False)