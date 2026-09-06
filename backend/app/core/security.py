import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from app.db.database import get_db
from app.models import Portfolio, User


SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key-change-me")
TOKEN_MAX_AGE = 60 * 60 * 24
token_serializer = URLSafeTimedSerializer(SECRET_KEY, salt="portfolio-auth")
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
	return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
	return check_password_hash(password_hash, password)


def create_access_token(user_id: int) -> str:
	return token_serializer.dumps({"user_id": user_id})


def get_current_user(
	credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
	db: Session = Depends(get_db),
) -> User:
	credentials_error = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Authentication required",
		headers={"WWW-Authenticate": "Bearer"},
	)

	if credentials is None:
		raise credentials_error

	try:
		payload = token_serializer.loads(
			credentials.credentials,
			max_age=TOKEN_MAX_AGE,
		)
		user_id = payload.get("user_id")
	except (BadSignature, SignatureExpired, TypeError, ValueError):
		raise credentials_error

	user = db.query(User).filter(User.id == user_id).first()
	if not user or not user.is_active:
		raise credentials_error

	return user


def get_owned_portfolio(
	portfolio_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
) -> Portfolio:
	portfolio = (
		db.query(Portfolio)
		.filter(
			Portfolio.id == portfolio_id,
			Portfolio.user_id == current_user.id,
		)
		.first()
	)

	if not portfolio:
		raise HTTPException(status_code=404, detail="Portfolio not found")

	return portfolio
