from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    blood_group: str
    city: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    blood_group: str
    city: str

    

class BloodRequestCreate(BaseModel):
    patient_name: str
    blood_group: str
    city: str
    hospital: str
    units_needed: int
    contact_phone: str

    class Config:
        from_attributes = True