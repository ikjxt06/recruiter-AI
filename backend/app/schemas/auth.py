from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(LoginRequest):
    full_name: str
    role: str = "recruiter"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
