from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user
from app.db.database import get_db
from app.models import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.auth_service import authenticate_user, create_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


def user_response(user: User) -> dict:
	return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
	email = payload.email.lower().strip()
	if db.query(User).filter(User.email == email).first():
		raise HTTPException(status_code=409, detail="Email is already registered")

	user = create_user(db, payload.name, email, payload.password)
	return {
		"access_token": create_access_token(user.id),
		"token_type": "bearer",
		"user": user_response(user),
	}


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
	user = authenticate_user(db, payload.email, payload.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid email or password",
			headers={"WWW-Authenticate": "Bearer"},
		)

	return {
		"access_token": create_access_token(user.id),
		"token_type": "bearer",
		"user": user_response(user),
	}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
	return user_response(current_user)
