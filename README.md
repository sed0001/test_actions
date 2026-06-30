# Test FastAPI Application

Тестовое REST API приложение на **FastAPI** с Docker-развёртыванием и CI/CD через GitHub Actions.

## 📋 Оглавление

- [Возможности](#-возможности)
- [Структура проекта](#-структура-проекта)
- [Быстрый старт](#-быстрый-старт)
- [API Endpoints](#-api-endpoints)
- [Docker](#-docker)
- [CI/CD](#-cicd)
- [Переменные окружения](#-переменные-окружения)

## ✨ Возможности

- RESTful API с CRUD операциями для ресурсов
- Автоматическая документация (Swagger / ReDoc)
- Docker-контейнеризация
- GitHub Actions для сборки и деплоя образов
- Pydantic v2 модели валидации

## 📁 Структура проекта

```
├── main.py              # Основное приложение FastAPI
├── requirements.txt     # Python зависимости
├── Dockerfile           # Docker-образ
├── .dockerignore        # Файлы для исключения из Docker
├── .github/
│   └── workflows/
│       └── deploy.yml   # GitHub Actions CI/CD
└── README.md            # Документация
```

## 🚀 Быстрый старт

### Локальный запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
uvicorn main:app --reload
```

### Через Docker

```bash
# Сборка образа
docker build -t fastapi-app .

# Запуск контейнера
docker run -d -p 8000:8000 --name fastapi fastapi-app
```

## 📡 API Endpoints

### Информация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/` | Корневой эндпоинт |
| `GET` | `/health` | Проверка работоспособности |
| `GET` | `/info` | Информация о приложении |
| `GET` | `/current-date` | Текущая дата |

### Items (CRUD)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/items` | Получить все элементы |
| `POST` | `/items` | Создать новый элемент |
| `GET` | `/items/{id}` | Получить элемент по ID |
| `PUT` | `/items/{id}` | Обновить элемент |
| `DELETE` | `/items/{id}` | Удалить элемент |

### Документация API

После запуска доступны:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🐳 Docker

### Dockerfile

- Базовый образ: `python:3.11-slim`
- Порт: `8000`
- Сервер: `uvicorn`

### .dockerignore

Исключает из образа:
- `.env` файлы
- `.git` и `.github`
- Python кэш (`__pycache__`, `.pyc`)
- IDE файлы
- Документацию

## 🔄 CI/CD

GitHub Actions автоматически:

1. **Собирает** Docker-образ при пуше в `main` или PR
2. **Пушит** образ в GitHub Container Registry (ghcr.io)
3. **Деплоит** на сервер через SSH (только для `main`)

### Необходимые Secrets

| Secret | Описание |
|--------|----------|
| `HOST` | IP/домен сервера |
| `USERNAME` | Имя пользователя для SSH |
| `SSH_KEY` | SSH приватный ключ |
| `PORT` | SSH порт |
| `ENVIRONMENT` | Окружение (production/development) |
| `DEBUG` | true/false |

## 🔧 Переменные окружения

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `ENVIRONMENT` | `development` | Текущее окружение |
| `DEBUG` | `false` | Режим отладки |
| `PORT` | `8000` | Порт сервера |

Создайте `.env` файл:

```env
ENVIRONMENT=development
DEBUG=true
PORT=8000
```

## 📝 Примеры запросов

### Создать элемент

```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "Test description"}'
```

### Получить все элементы

```bash
curl http://localhost:8000/items
```

### Обновить элемент

```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'
```

### Удалить элемент

```bash
curl -X DELETE http://localhost:8000/items/1
```

## 🛠 Технологии

- **Python 3.11**
- **FastAPI** — современный web-фреймворк
- **Pydantic v2** — валидация данных
- **Uvicorn** — ASGI сервер
- **Docker** — контейнеризация
- **GitHub Actions** — CI/CD

## 📄 License

MIT
