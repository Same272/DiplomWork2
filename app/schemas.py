from pydantic import BaseModel
from typing import Optional, List

# Схема для регистрации пользователя
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str

# Схема для билета
class TicketBase(BaseModel):
    title: str
    description: str
    price: float
    available_seats: int
    is_vip: bool

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int

    class Config:
        orm_mode = True

# Схема для бронирования
class BookingBase(BaseModel):
    ticket_id: int
    num_passengers: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True