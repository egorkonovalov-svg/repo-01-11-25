# Инструкция по запуску приложения с фронтендом

## Предварительные требования

1. Python 3.8+
2. PostgreSQL (или используйте Docker Compose)
3. Установленные зависимости

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Настройка базы данных

Создайте файл `.env` в папке `env/` со следующим содержимым:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=finances
SECRET_TOKEN=your_secret_token_here
```

Или используйте Docker Compose для запуска базы данных:

```bash
docker-compose up -d db
```

## Шаг 3: Применение миграций базы данных

```bash
alembic upgrade head
```

## Шаг 4: Запуск приложения

### Вариант 1: Используя скрипт запуска (Windows)

```bash
start.bat
```

### Вариант 2: Используя скрипт запуска (Linux/Mac)

```bash
chmod +x start.sh
./start.sh
```

### Вариант 3: Используя run_server.py

```bash
cd backend
python run_server.py
```

### Вариант 4: Используя uvicorn напрямую

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Вариант 5: Из корня проекта

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Шаг 5: Открытие в браузере

После запуска откройте в браузере:

- **Главная страница**: http://localhost:8000/
- **Страница входа**: http://localhost:8000/login
- **Страница регистрации**: http://localhost:8000/register
- **API документация**: http://localhost:8000/docs

## Структура фронтенда

- `backend/templates/` - HTML шаблоны (Jinja2)
- `backend/static/` - CSS и JavaScript файлы

## Доступные страницы

- `/` - Главная страница со сводкой
- `/transactions` - Управление транзакциями
- `/categories` - Управление категориями
- `/budgets` - Управление бюджетами
- `/goals` - Управление целями
- `/login` - Страница входа
- `/register` - Страница регистрации

## API эндпоинты

Все API эндпоинты доступны по адресу `/api/v1/...`:
- `/api/v1/auth/*` - Аутентификация
- `/api/v1/transaction/*` - Транзакции
- `/api/v1/category/*` - Категории
- `/api/v1/budget/*` - Бюджеты
- `/api/v1/goal/*` - Цели

## Примечания

- Приложение использует cookie-аутентификацию
- После успешного входа/регистрации происходит автоматическое перенаправление на главную страницу
- Все формы отправляются через AJAX и автоматически обновляют страницу после успешного выполнения

