import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, Token

SECRET_KEY = os.getenv("SECRET_KEY", "cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def _hash(self, password: str) -> str:
        return _pwd.hash(password)

    def _verify(self, plain: str, hashed: str) -> bool:
        return _pwd.verify(plain, hashed)

    def _create_token(self, username: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
            return username
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def register(self, db: Session, data: UserCreate) -> dict:
        repo = UserRepository(db)
        if repo.get_by_username(data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe")
        if repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado")
        user = repo.create(data.username, data.email, self._hash(data.password))
        return {"id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active}

    def login(self, db: Session, username: str, password: str) -> Token:
        repo = UserRepository(db)
        user = repo.get_by_username(username)
        if not user or not self._verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
        return Token(access_token=self._create_token(user.username))


auth_service = AuthService()
