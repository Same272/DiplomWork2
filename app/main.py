from fastapi import FastAPI
from .routers import tickets  # Импортируем роутер
from .database import engine, Base  # Импортируем engine и Base для создания таблиц в базе данных

# Создаем все таблицы в базе данных, если они еще не созданы
Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI
app = FastAPI(docs_url='/')

# Подключаем роутер для работы с билетами и бронированием
app.include_router(tickets.router, prefix="/api")

# Опционально: Добавляем описание и метаданные для документации API
app.title = "Ticket Sale API"
app.description = "API для продажи билетов с регистрацией, авторизацией и бронированием."
app.version = "1.0.0"