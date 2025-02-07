import secrets
import hashlib
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

# Секретный ключ для подписи токенов
SECRET_KEY = secrets.token_hex(32)  # Генерируем случайный секретный ключ
ALGORITHM = "HS256"  # Используем HMAC-SHA256 для подписи токенов
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для создания токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})  # Добавляем время истечения
    # Преобразуем данные в строку и хэшируем
    token_data = f"{to_encode}".encode("utf-8")
    token = hashlib.sha256(token_data + SECRET_KEY.encode("utf-8")).hexdigest()
    return token

# Функция для проверки токена
def verify_token(token: str, db: Session = Depends(get_db)):
    try:
        # Проверяем, что токен существует и соответствует ожидаемому формату
        # В реальном приложении здесь нужно добавить логику проверки подписи и времени истечения
        user = db.query(models.User).filter(models.User.hashed_password == token).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )