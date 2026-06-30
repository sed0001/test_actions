# main.py
# Тестовое FastAPI приложение

import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Загружаем переменные из .env
load_dotenv()

# === Pydantic модели ===
class ItemCreate(BaseModel):
    """Модель для создания/обновления элемента."""
    name: str
    description: Optional[str] = None

class Item(BaseModel):
    """Модель для ответа с элементом."""
    id: int
    name: str
    description: Optional[str] = None

# === In-memory хранилище ===
items_db: List[Item] = [
    {"id": 1, "name": "Item 1", "description": "Description 1"},
    {"id": 2, "name": "Item 2", "description": "Description 2"},
]

# === Создание приложения ===
app = FastAPI(
    title="Test FastAPI Application",
    version="1.0.2",
    description="Тестовое приложение для демонстрации работы FastAPI и Docker"
)

# === Эндпоинты ===

@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "Добро пожаловать в Test FastAPI Application"}

@app.get("/health")
async def health_check():
    """Проверка работоспособности. изменение2"""
    return {"status": "ok"}

# ===== CRUD для items =====

@app.get("/items", response_model=List[Item])
async def get_items():
    """Получить список всех элементов."""
    return items_db

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Создать новый элемент."""
    new_id = max((i["id"] for i in items_db), default=0) + 1
    new_item = Item(id=new_id, **item.dict())
    items_db.append(new_item.dict())
    return new_item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Получить элемент по ID."""
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Элемент не найден")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: ItemCreate):
    """Обновить элемент по ID."""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db[i] = {"id": item_id, **updated_item.dict()}
            return items_db[i]
    raise HTTPException(status_code=404, detail="Элемент не найден")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Удалить элемент по ID."""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Элемент '{deleted_item['name']}' удален"}
    raise HTTPException(status_code=404, detail="Элемент не найден")

# ===== Дополнительные эндпоинты =====

@app.get("/info")
async def get_info():
    """Получить информацию о приложении."""
    return {
        "app_name": "Test FastAPI Application",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "false").lower() == "true"
    }

@app.get("/current-date")
async def get_current_date():
    """Получить текущую дату."""
    return {
        "app_name": "Test FastAPI Application",
        "version": "1.0.0",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "debug": os.getenv("DEBUG", "false").lower() == "true"
    }

# === Запуск приложения ===
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )