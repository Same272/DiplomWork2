from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Инициализация контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для получения пользователя по имени
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# Функция для создания пользователя
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Функция для аутентификации пользователя
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username=username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


# Функция для получения билета по ID
def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()


# Функция для получения списка билетов с фильтрацией по категории и типу
def get_tickets(db: Session, category: str = None, is_vip: bool = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Ticket)
    if category:
        query = query.filter(models.Ticket.category == category)
    if is_vip is not None:
        query = query.filter(models.Ticket.is_vip == is_vip)
    return query.offset(skip).limit(limit).all()


# Функция для создания билета
def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


# Функция для создания бронирования
def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):
    ticket = get_ticket(db, booking.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.available_seats < booking.num_passengers:
        raise HTTPException(status_code=400, detail="Not enough available seats")
    if booking.seat_type == "VIP" and not ticket.is_vip:
        raise HTTPException(status_code=400, detail="This ticket is not VIP")

    db_booking = models.Booking(**booking.dict(), user_id=user_id)
    ticket.available_seats -= booking.num_passengers
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking