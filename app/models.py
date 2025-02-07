from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    bookings = relationship("Booking", back_populates="user")

# Модель билета
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    available_seats = Column(Integer)
    is_vip = Column(Boolean, default=False)
    category = Column(String)  # Добавляем категорию билета

    bookings = relationship("Booking", back_populates="ticket")

# Модель бронирования
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    num_passengers = Column(Integer)  # Количество людей
    seat_type = Column(String)  # Тип места (VIP или обычный)

    user = relationship("User", back_populates="bookings")
    ticket = relationship("Ticket", back_populates="bookings")