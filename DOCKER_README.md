# Запуск приложения в Docker

## Быстрый старт

1. Создайте файл `.env` в корне проекта (или используйте переменные окружения):

```env
DB_NAME=finances
DB_USER=postgres
DB_PASSWORD=postgres
SECRET_TOKEN=your-secret-token-here
YANDEX_API=your-yandex-api-key
```

2. Запустите приложение:

```bash
docker-compose up -d
```

3. Откройте в браузере:
   - Главная страница: http://localhost:8000/
   - API документация: http://localhost:8000/docs

## Команды

### Запуск
```bash
docker-compose up -d
```

### Остановка
```bash
docker-compose stop
```

### Остановка и удаление контейнеров
```bash
docker-compose down
```

### Просмотр логов
```bash
docker-compose logs -f backend
```

### Пересборка образов
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Применение миграций вручную
```bash
docker-compose exec backend alembic upgrade head
```

## Структура

- `backend/Dockerfile` - образ для backend приложения
- `docker-compose.yml` - конфигурация для всех сервисов
- `backend/docker-entrypoint.sh` - скрипт инициализации при запуске

## Переменные окружения

Все переменные можно задать в файле `.env` или передать через `docker-compose.yml`:

- `DB_NAME` - имя базы данных (по умолчанию: finances)
- `DB_USER` - пользователь БД (по умолчанию: postgres)
- `DB_PASSWORD` - пароль БД (по умолчанию: postgres)
- `SECRET_TOKEN` - секретный ключ для JWT (обязательно измените!)
- `YANDEX_API` - API ключ Yandex (опционально)

## Примечания

- База данных автоматически создается при первом запуске
- Миграции применяются автоматически при запуске контейнера
- Данные базы данных сохраняются в Docker volume `postgres_data`
- Фронтенд встроен в backend и доступен на порту 8000

