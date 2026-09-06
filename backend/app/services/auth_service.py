from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models import User


def create_user(db: Session, name: str, email: str, password: str) -> User:
	user = User(
		name=name.strip(),
		email=email.lower().strip(),
		password_hash=hash_password(password),
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
	user = (
		db.query(User)
		.filter(User.email == email.lower().strip())
		.first()
	)
	if not user or not verify_password(password, user.password_hash):
		return None
	return user
