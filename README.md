
# Трекер Финансов

## Описание
проект - приложение для отслеживания финансов и трат

## Технологии
Список используемых технологий и инструментов:
* Язык программирования: Python
* Фреймворки: FastAPI, SQLAlchemy, jinja2
* Библиотеки: Alembic, PyDantic, uvicorn, authx...
* Базы данных: PostgreSQL + asyncpg
* Тестирование: pytest + httpx
* Контейнеры: Docker

[//]: # (* Другие инструменты)

## Установка
### Требования
Требования находятся в папке requirements.txt в корне проекта.

### Установка
Пошаговая инструкция по установке проекта:
1. Клонирование репозитория
```bash
git clone https://github.com/egorkonovalov-svg/repo-01-11-25.git
```
2. установка вирутального окружения
```bash
python3 -m venv venv 
```
3. файл .env
   -Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=xxxx
DB_PASSWORD=xxxx
DB_NAME=xxxx
 -JWT Secret Token
SECRET_TOKEN=xxxx


5. запуск через докер
```bash
docker-compose up --build
```
