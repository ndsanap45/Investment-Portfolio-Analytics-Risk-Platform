from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	email: str = Field(min_length=3, max_length=255)
	password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
	email: str = Field(min_length=3, max_length=255)
	password: str = Field(min_length=1, max_length=128)


class AuthResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"
	user: dict
