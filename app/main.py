from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes.auth_routes import router as auth_router
from app.routes.donor_routes import router as donor_router
from app.routes.request_routes import router as request_router
from app.routes.user_routes import router as user_router
from app.routes.response_routes import router as response_router
from app.routes.notification_routes import router as notification_router
from app.routes.admin_routes import router as admin_router
from app.routes.admin_user_routes import (
    router as admin_user_router
)


from app.models import User
from app.request_models import BloodRequest
from app.response_models import RequestResponse

app = FastAPI(
    title="LifeLink Blood Donation API",
    description="Blood Donation and Emergency Request Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://your-vercel-app.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(donor_router)
app.include_router(request_router)
app.include_router(user_router)
app.include_router(response_router)
app.include_router(notification_router)
app.include_router(admin_router)
app.include_router(admin_user_router)


@app.get("/")
def home():
    return {
        "message": "LifeLink API Running"
    }