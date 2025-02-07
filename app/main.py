from fastapi import FastAPI
from .routers import tickets
from .database import engine, Base

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI
app = FastAPI()

# Подключаем роутер
app.include_router(tickets.router, prefix="/api")