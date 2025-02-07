from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import schemas, crud, database
from ..models import User
from ..security import create_access_token, verify_token, oauth2_scheme

router = APIRouter()

# Эндпоинт для регистрации пользователя
@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

# Эндпоинт для получения токена
@router.post("/token/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Эндпоинт для получения текущего пользователя
@router.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: User = Depends(verify_token)):
    return current_user

# Эндпоинт для создания билета
@router.post("/tickets/", response_model=schemas.Ticket)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    return crud.create_ticket(db, ticket)

# Эндпоинт для получения списка билетов
@router.get("/tickets/", response_model=List[schemas.Ticket])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets

# Эндпоинт для бронирования билета
@router.post("/book/", response_model=schemas.Booking)
def book_ticket(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user: User = Depends(verify_token)):
    ticket = crud.get_ticket(db, booking.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.available_seats < booking.num_passengers:
        raise HTTPException(status_code=400, detail="Not enough available seats")
    return crud.create_booking(db, booking, current_user.id)