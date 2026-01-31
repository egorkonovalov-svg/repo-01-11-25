# ДОКУМЕНТАЦИЯ ПРОЕКТА "ТРЕКЕР ФИНАНСОВ"

## Подробное описание работы приложения для реферата

---

## СОДЕРЖАНИЕ

1. [Общее описание проекта](#1-общее-описание-проекта)
2. [Структура проекта](#2-структура-проекта)
3. [База данных](#3-база-данных)
4. [Серверная часть (Backend)](#4-серверная-часть-backend)
5. [Клиентская часть (Frontend)](#5-клиентская-часть-frontend)
6. [Система безопасности](#6-система-безопасности)
7. [Как работает приложение](#7-как-работает-приложение)
8. [Запуск приложения](#8-запуск-приложения)

---

## 1. ОБЩЕЕ ОПИСАНИЕ ПРОЕКТА

### Что это за приложение?

"Трекер Финансов" — это веб-приложение для учёта личных денег. Оно помогает людям:
- Записывать свои доходы (зарплата, подарки, продажи)
- Записывать свои расходы (еда, транспорт, развлечения)
- Видеть сколько денег осталось (баланс)
- Ставить финансовые цели (накопить на телефон, поездку)
- Планировать бюджет (не тратить больше определённой суммы в месяц)

### Какие технологии используются?

| Технология | Для чего нужна |
|------------|----------------|
| Python | Основной язык программирования |
| FastAPI | Создание веб-сервера (принимает запросы от браузера) |
| PostgreSQL | База данных (хранит все данные пользователей) |
| SQLAlchemy | Работа с базой данных через Python |
| HTML/CSS/JavaScript | Создание веб-страниц |
| Jinja2 | Шаблоны для HTML-страниц |
| Docker | Упаковка приложения в контейнер для запуска |
| JWT | Безопасная авторизация пользователей |

---

## 2. СТРУКТУРА ПРОЕКТА

Проект разделён на две основные части:

```
repo-01-11-25/
│
├── backend/                 # Серверная часть (Python)
│   ├── main.py             # Главный файл приложения
│   ├── database.py         # Подключение к базе данных
│   ├── crypt_module.py     # Шифрование паролей
│   ├── dependencies.py     # Проверка авторизации
│   │
│   ├── models/             # Модели данных (таблицы в базе)
│   │   ├── user.py         # Пользователь
│   │   ├── transaction.py  # Транзакция (доход/расход)
│   │   ├── category.py     # Категория
│   │   ├── budget.py       # Бюджет
│   │   └── goal.py         # Цель
│   │
│   ├── routers/            # Обработчики запросов
│   │   ├── user_router.py
│   │   ├── transaction_router.py
│   │   ├── category_router.py
│   │   ├── budget_router.py
│   │   └── goal_router.py
│   │
│   └── services/           # Бизнес-логика (работа с данными)
│       ├── user_service.py
│       ├── transaction_service.py
│       ├── category_service.py
│       ├── budget_service.py
│       └── goal_service.py
│
├── frontend/               # Клиентская часть (HTML/CSS/JS)
│   ├── templates/          # HTML-шаблоны страниц
│   │   ├── layout.html     # Общий шаблон (меню, подвал)
│   │   ├── index.html      # Главная страница
│   │   ├── login.html      # Страница входа
│   │   ├── register.html   # Страница регистрации
│   │   ├── transactions.html
│   │   ├── categories.html
│   │   ├── budgets.html
│   │   └── goals.html
│   │
│   └── static/             # Статические файлы
│       ├── style.css       # Стили оформления
│       └── script.js       # JavaScript функции
│
├── docker-compose.yml      # Настройки Docker
└── README.md               # Краткое описание проекта
```

---

## 3. БАЗА ДАННЫХ

### Что такое база данных?

База данных — это место, где хранятся все данные приложения. Можно представить её как набор связанных таблиц (похожих на Excel).

### Какие таблицы есть в приложении?

#### Таблица 1: users (Пользователи)

Хранит информацию о зарегистрированных пользователях.

| Поле | Тип данных | Описание |
|------|------------|----------|
| id | Число | Уникальный номер пользователя |
| UserName | Текст | Имя пользователя для входа |
| Email | Текст | Электронная почта |
| PasswordHash | Байты | Зашифрованный пароль |
| Name | Текст | Настоящее имя |

**Код модели (файл `models/user.py`):**

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    UserName = Column(String, unique=True)
    Email = Column(String())
    PasswordHash = Column(LargeBinary())
    Name = Column(String())
```

Что здесь происходит:
- `__tablename__ = "users"` — название таблицы в базе данных
- `primary_key=True` — это главный ключ (уникальный идентификатор)
- `unique=True` — значение не может повторяться у разных пользователей
- `LargeBinary()` — хранит пароль в зашифрованном виде (не обычный текст!)

---

#### Таблица 2: transactions (Транзакции)

Хранит все доходы и расходы пользователя.

| Поле | Тип данных | Описание |
|------|------------|----------|
| id | Число | Уникальный номер транзакции |
| amount | Дробное число | Сумма денег |
| description | Текст | Описание (за что) |
| date | Дата | Когда произошла транзакция |
| type | Выбор | Тип: "income" (доход) или "expense" (расход) |
| user_id | Число | Номер пользователя (чья это транзакция) |
| category_id | Число | Номер категории |
| tags | Текст | Метки через запятую |

**Код модели (файл `models/transaction.py`):**

```python
class TransactionType(enum.Enum):
    INCOME = "income"      # Доход
    EXPENSE = "expense"    # Расход

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255))
    date = Column(Date, nullable=False, index=True)
    type = Column(Enum(TransactionType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    tags = Column(String(255))
```

Что здесь происходит:
- `TransactionType` — это перечисление (enum), которое ограничивает выбор только двумя вариантами
- `nullable=False` — поле обязательно для заполнения
- `ForeignKey("users.id")` — связь с таблицей пользователей. Это означает, что каждая транзакция принадлежит какому-то пользователю
- `index=True` — создаёт индекс для быстрого поиска по дате

---

#### Таблица 3: categories (Категории)

Хранит категории для группировки транзакций (еда, транспорт, зарплата).

| Поле | Тип данных | Описание |
|------|------------|----------|
| id | Число | Уникальный номер категории |
| name | Текст | Название категории |
| description | Текст | Описание |
| type | Выбор | Для доходов или расходов |
| is_default | Да/Нет | Категория по умолчанию |
| user_id | Число | Чья это категория |

**Код модели (файл `models/category.py`):**

```python
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(Enum(TransactionType), nullable=False)
    is_default = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

Что здесь происходит:
- `String(100)` — текст максимум 100 символов
- `Text` — текст без ограничения длины
- `Boolean` — логическое значение (да/нет, true/false)
- `default=False` — значение по умолчанию, если не указано другое

---

#### Таблица 4: budgets (Бюджеты)

Хранит планы расходов на определённый период.

| Поле | Тип данных | Описание |
|------|------------|----------|
| id | Число | Уникальный номер |
| name | Текст | Название бюджета |
| amount | Дробное число | Лимит денег |
| period | Выбор | Период: день/неделя/месяц/год |
| start_date | Дата | Дата начала |
| end_date | Дата | Дата окончания |
| is_active | Да/Нет | Активен ли бюджет |
| user_id | Число | Чей это бюджет |
| category_id | Число | Для какой категории |

**Код модели (файл `models/budget.py`):**

```python
class BudgetPeriod(enum.Enum):
    DAILY = "daily"        # Ежедневно
    WEEKLY = "weekly"      # Еженедельно
    MONTHLY = "monthly"    # Ежемесячно
    YEARLY = "yearly"      # Ежегодно

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    period = Column(Enum(BudgetPeriod), default=BudgetPeriod.MONTHLY)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
```

---

#### Таблица 5: goals (Цели)

Хранит финансовые цели пользователя.

| Поле | Тип данных | Описание |
|------|------------|----------|
| id | Число | Уникальный номер |
| name | Текст | Название цели |
| target_amount | Дробное число | Сколько нужно накопить |
| current_amount | Дробное число | Сколько уже накоплено |
| deadline | Дата | Крайний срок |
| description | Текст | Описание цели |
| is_completed | Да/Нет | Достигнута ли цель |
| user_id | Число | Чья это цель |

**Код модели (файл `models/goal.py`):**

```python
class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline = Column(Date)
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

---

### Как таблицы связаны между собой?

```
┌─────────────┐
│   USERS     │
│ (Пользова-  │
│   тели)     │
└──────┬──────┘
       │ Один пользователь имеет много:
       │
       ├──────────────────┬──────────────────┬─────────────────┐
       │                  │                  │                 │
       ▼                  ▼                  ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ TRANSACTIONS│   │ CATEGORIES  │   │  BUDGETS    │   │   GOALS     │
│ (Транзакции)│   │ (Категории) │   │ (Бюджеты)   │   │  (Цели)     │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └─────────────┘
       │                 │                 │
       │                 │                 │
       └────────────────►│◄────────────────┘
                         │
            Транзакции и Бюджеты
            используют Категории
```

---

### Подключение к базе данных

**Файл `database.py`:**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from services.config import DATABASE_URL
from models.base import Base

# Создаём "движок" для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём фабрику сессий (сессия = одно подключение к базе)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db(): 
    """Создаёт все таблицы в базе данных"""
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.drop_all)   # Удаляет старые таблицы
        await conn.run_sync(Base.metadata.create_all) # Создаёт новые таблицы

async def get_db():
    """Выдаёт сессию для работы с базой"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
```

Что здесь происходит:
- `create_async_engine` — создаёт асинхронное подключение к базе данных
- `async_sessionmaker` — создаёт "фабрику" сессий. Каждая сессия — это одно подключение к базе
- `echo=True` — выводит все SQL-запросы в консоль (для отладки)
- `init_db()` — функция, которая создаёт таблицы при запуске приложения

---

## 4. СЕРВЕРНАЯ ЧАСТЬ (BACKEND)

### Что такое Backend?

Backend (серверная часть) — это код, который работает на сервере. Он:
- Принимает запросы от браузера
- Обрабатывает данные
- Работает с базой данных
- Отправляет ответы обратно в браузер

### Главный файл приложения (main.py)

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Создаём приложение FastAPI
app = FastAPI(title='finance-src', lifespan=lifespan, debug=True)

# Настраиваем шаблоны и статические файлы
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")

# Подключаем роутеры (обработчики запросов)
app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(budget_router)
app.include_router(category_router)
app.include_router(goal_router)
```

Что здесь происходит:
- `FastAPI()` — создаём веб-приложение
- `Jinja2Templates` — подключаем шаблоны HTML
- `StaticFiles` — даём доступ к CSS и JavaScript файлам
- `include_router` — подключаем обработчики для разных URL-адресов

### Пример страницы (главная)

```python
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница со сводкой"""
    try:
        # Проверяем, авторизован ли пользователь
        user_id = await get_user_id_from_cookie(request.cookies.get("access_token"))
    except:
        # Если не авторизован — отправляем на страницу входа
        return RedirectResponse(url="/login", status_code=303)
    
    # Получаем данные из базы
    summary = await get_transactions_summary(user_id, None, None)
    goals = await get_user_goals(user_id, None)
    budgets = await get_user_budgets(user_id, None, None)
    
    # Отправляем HTML-страницу с данными
    return templates.TemplateResponse("index.html", {
        "request": request,
        "summary": summary,
        "goals": goals[:5],
        "budgets": budgets[:5]
    })
```

Что здесь происходит:
1. `@app.get("/")` — этот код выполняется когда пользователь открывает главную страницу
2. Проверяем авторизацию через cookie (маленький файл в браузере)
3. Если не авторизован — отправляем на страницу входа
4. Загружаем данные из базы (сводка, цели, бюджеты)
5. Отправляем HTML-страницу с этими данными

---

### Роутеры (Обработчики запросов)

Роутер — это набор функций, которые обрабатывают запросы на определённые URL-адреса.

#### Роутер пользователей (user_router.py)

Отвечает за регистрацию, вход и выход из системы.

```python
user_router = APIRouter(prefix='/api/v1/auth')

@user_router.post("/register")
async def register(data: RegisterRequest, response: Response):
    """Регистрация нового пользователя"""
    # Создаём пользователя и получаем токен
    jwt_token = await register_user(data)
    
    if jwt_token and jwt_token != 'error':
        # Сохраняем токен в cookie браузера
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,      # JavaScript не может прочитать
            secure=True,        # Только через HTTPS
            samesite="lax",     # Защита от атак
            max_age=7 * 24 * 60 * 60  # Живёт 7 дней
        )
        return {"message": "Registration successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=400, detail="Registration failed")


@user_router.post("/login")
async def login(data: LoginRequest, response: Response):
    """Вход в систему"""
    jwt_token = await login_check(data)
    
    if jwt_token and jwt_token != 'error':
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )
        return {"message": "Login successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@user_router.post("/logout")
async def logout(response: Response):
    """Выход из системы"""
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}
```

Что здесь происходит:
- `prefix='/api/v1/auth'` — все URL начинаются с /api/v1/auth
- `@user_router.post("/register")` — обрабатывает POST-запрос на /api/v1/auth/register
- `set_cookie` — сохраняет токен в браузере
- `delete_cookie` — удаляет токен при выходе

---

#### Роутер транзакций (transaction_router.py)

Отвечает за создание, чтение, обновление и удаление транзакций.

```python
transaction_router = APIRouter(prefix='/api/v1/transaction')

@transaction_router.post("/", response_model=TransactionResponse)
async def create_transaction_endpoint(
    data: TransactionCreate,
    user_id: int = Depends(get_current_user_id)
):
    """Создать новую транзакцию"""
    return await create_transaction(user_id, data)


@transaction_router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    start_date: Optional[date] = Query(None, description="Начальная дата"),
    end_date: Optional[date] = Query(None, description="Конечная дата"),
    category_id: Optional[int] = Query(None, description="ID категории"),
    type: Optional[TransactionType] = Query(None, description="Тип транзакции"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    offset: int = Query(0, ge=0, description="Смещение"),
    user_id: int = Depends(get_current_user_id)
):
    """Получить транзакции пользователя с фильтрами"""
    return await get_user_transactions(
        user_id, start_date, end_date, category_id, type, limit, offset
    )


@transaction_router.delete("/{transaction_id}")
async def delete_transaction_endpoint(
    transaction_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Удалить транзакцию"""
    await delete_transaction(transaction_id, user_id)
    return {"message": "Transaction deleted successfully"}
```

Что здесь происходит:
- `Depends(get_current_user_id)` — автоматически проверяет авторизацию и получает ID пользователя
- `Query()` — параметры, которые передаются в URL (например, ?start_date=2025-01-01)
- `response_model=TransactionResponse` — указывает формат ответа

---

### Сервисы (Бизнес-логика)

Сервисы — это функции, которые выполняют основную работу с данными.

#### Сервис транзакций (transaction_service.py)

```python
async def create_transaction(user_id: int, data: TransactionCreate) -> Transaction:
    """Создать новую транзакцию"""
    async with async_session_maker() as session:
        # Создаём новый объект транзакции
        new_transaction = Transaction(
            amount=data.amount,
            description=data.description,
            date=data.date,
            type=data.type,
            category_id=data.category_id,
            user_id=user_id,
            tags=data.tags
        )
        # Добавляем в сессию
        session.add(new_transaction)
        # Сохраняем в базу
        await session.commit()
        # Обновляем объект (получаем ID из базы)
        await session.refresh(new_transaction)
        return new_transaction
```

Что здесь происходит:
1. `async with async_session_maker() as session` — открываем подключение к базе
2. Создаём объект Transaction с данными
3. `session.add()` — добавляем в очередь на сохранение
4. `session.commit()` — сохраняем изменения в базу
5. `session.refresh()` — обновляем объект (теперь у него есть ID)

---

#### Получение списка транзакций с фильтрами

```python
async def get_user_transactions(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    type: Optional[TransactionType] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Transaction]:
    """Получить транзакции пользователя с фильтрами"""
    async with async_session_maker() as session:
        # Начинаем строить запрос
        query = select(Transaction).where(Transaction.user_id == user_id)
        
        # Добавляем фильтры если они указаны
        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)
        if category_id:
            query = query.where(Transaction.category_id == category_id)
        if type:
            query = query.where(Transaction.type == type)
        
        # Сортируем по дате (новые сначала) и ограничиваем количество
        query = query.order_by(Transaction.date.desc()).limit(limit).offset(offset)
        
        # Выполняем запрос
        result = await session.execute(query)
        return list(result.scalars().all())
```

Что здесь происходит:
1. `select(Transaction)` — начинаем SELECT-запрос к таблице transactions
2. `.where()` — добавляем условия (WHERE в SQL)
3. `.order_by(Transaction.date.desc())` — сортировка по дате, новые сначала
4. `.limit(limit).offset(offset)` — ограничение количества результатов
5. `session.execute()` — выполняем запрос
6. `result.scalars().all()` — получаем список объектов

---

#### Подсчёт итогов (доходы, расходы, баланс)

```python
async def get_transactions_summary(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> dict:
    """Получить сводку по транзакциям (доходы и расходы)"""
    async with async_session_maker() as session:
        # Запрос с группировкой по типу и суммированием
        query = select(
            Transaction.type,
            func.sum(Transaction.amount).label('total')
        ).where(Transaction.user_id == user_id)
        
        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)
        
        # Группируем по типу транзакции
        query = query.group_by(Transaction.type)
        result = await session.execute(query)
        
        # Собираем результат
        summary = {"income": 0.0, "expense": 0.0}
        for row in result.all():
            if row.type == TransactionType.INCOME:
                summary["income"] = float(row.total or 0)
            elif row.type == TransactionType.EXPENSE:
                summary["expense"] = float(row.total or 0)
        
        # Считаем баланс
        summary["balance"] = summary["income"] - summary["expense"]
        return summary
```

Что здесь происходит:
1. `func.sum()` — функция суммирования (SUM в SQL)
2. `.group_by()` — группировка результатов
3. Считаем отдельно доходы и расходы
4. Баланс = Доходы - Расходы

---

#### Сервис целей (goal_service.py)

```python
async def add_amount_to_goal(goal_id: int, user_id: int, amount: float) -> Goal:
    """Добавить сумму к текущему прогрессу цели"""
    async with async_session_maker() as session:
        # Находим цель
        query = select(Goal).where(
            Goal.id == goal_id,
            Goal.user_id == user_id
        )
        result = await session.execute(query)
        goal = result.scalars().first()
        
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        # Добавляем сумму
        goal.current_amount += amount
        
        # Проверяем, достигнута ли цель
        if goal.current_amount >= goal.target_amount:
            goal.is_completed = True
        
        await session.commit()
        await session.refresh(goal)
        return goal
```

Что здесь происходит:
1. Находим цель по ID и проверяем, что она принадлежит пользователю
2. Добавляем сумму к текущему прогрессу
3. Если накоплено >= цели, помечаем как выполненную
4. Сохраняем изменения

---

## 5. КЛИЕНТСКАЯ ЧАСТЬ (FRONTEND)

### Что такое Frontend?

Frontend (клиентская часть) — это то, что видит пользователь в браузере:
- HTML — структура страницы
- CSS — внешний вид (цвета, размеры, расположение)
- JavaScript — интерактивность (кнопки, формы)

### Шаблоны HTML (Jinja2)

Jinja2 — это система шаблонов. Она позволяет вставлять данные из Python в HTML.

#### Главный шаблон (layout.html)

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Финансовое приложение{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1 class="logo">Финансы</h1>
            <ul class="nav-menu">
                <li><a href="/">Главная</a></li>
                <li><a href="/transactions">Транзакции</a></li>
                <li><a href="/categories">Категории</a></li>
                <li><a href="/budgets">Бюджеты</a></li>
                <li><a href="/goals">Цели</a></li>
                <li><a href="#" onclick="logout(); return false;">Выход</a></li>
            </ul>
        </div>
    </nav>

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Финансовое приложение</p>
        </div>
    </footer>

    <script src="/static/script.js"></script>
</body>
</html>
```

Что здесь происходит:
- `{% block title %}` — место для заголовка страницы (заменяется в дочерних шаблонах)
- `{% block content %}` — место для основного содержимого
- `<nav>` — меню навигации
- `<main>` — основное содержимое
- `<footer>` — подвал страницы

---

#### Главная страница (index.html)

```html
{% extends "layout.html" %}

{% block title %}Главная - Финансовое приложение{% endblock %}

{% block content %}
<h2>Добро пожаловать!</h2>

<div class="stats-grid">
    <div class="stat-card">
        <h3>Доходы</h3>
        <div class="amount">{{ "%.2f"|format(summary.income) }} ₽</div>
    </div>
    <div class="stat-card">
        <h3>Расходы</h3>
        <div class="amount">{{ "%.2f"|format(summary.expense) }} ₽</div>
    </div>
    <div class="stat-card">
        <h3>Баланс</h3>
        <div class="amount">{{ "%.2f"|format(summary.balance) }} ₽</div>
    </div>
</div>
{% endblock %}
```

Что здесь происходит:
- `{% extends "layout.html" %}` — наследуем от главного шаблона
- `{{ summary.income }}` — выводим данные из Python
- `"%.2f"|format()` — форматируем число с двумя знаками после запятой

---

#### Страница целей (goals.html)

```html
{% extends "layout.html" %}

{% block content %}
<h2>Цели</h2>

<!-- Форма добавления цели -->
<div class="card">
    <div class="card-header">Добавить цель</div>
    <form id="goal-form" action="/api/v1/goal/" method="POST">
        <div class="form-group">
            <label>Название</label>
            <input type="text" name="name" required>
        </div>
        <div class="form-group">
            <label>Целевая сумма</label>
            <input type="number" name="target_amount" step="0.01" required>
        </div>
        <div class="form-group">
            <label>Срок</label>
            <input type="date" name="deadline" required>
        </div>
        <button type="submit" class="btn btn-primary">Добавить</button>
    </form>
</div>

<!-- Таблица целей -->
<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Название</th>
                <th>Прогресс</th>
                <th>Целевая сумма</th>
                <th>Срок</th>
                <th>Статус</th>
                <th>Действия</th>
            </tr>
        </thead>
        <tbody>
            {% if goals %}
                {% for goal in goals %}
                <tr>
                    <td><strong>{{ goal.name }}</strong></td>
                    <td>
                        <strong>{{ "%.2f"|format(goal.current_amount) }} ₽</strong>
                        {% set progress = [goal.current_amount / goal.target_amount * 100, 100]|min %}
                        <div style="background: white; border: 1px solid black; height: 20px;">
                            <div class="progress-bar" style="width: {{ progress }}%;">
                                {{ "%.0f"|format(progress) }}%
                            </div>
                        </div>
                    </td>
                    <td>{{ "%.2f"|format(goal.target_amount) }} ₽</td>
                    <td>{{ goal.deadline }}</td>
                    <td>{{ 'Выполнено' if goal.is_completed else 'В процессе' }}</td>
                    <td>
                        <button class="btn btn-danger btn-small" 
                                onclick="deleteItem('/api/v1/goal/{{ goal.id }}', 'цель')">
                            Удалить
                        </button>
                    </td>
                </tr>
                {% endfor %}
            {% else %}
                <tr>
                    <td colspan="6" class="empty-state">Нет целей</td>
                </tr>
            {% endif %}
        </tbody>
    </table>
</div>
{% endblock %}
```

Что здесь происходит:
- `{% for goal in goals %}` — цикл по всем целям
- `{% set progress = ... %}` — вычисляем процент выполнения
- `{{ 'Выполнено' if goal.is_completed else 'В процессе' }}` — условный вывод текста
- `onclick="deleteItem(...)"` — вызов JavaScript функции при клике

---

### JavaScript (script.js)

```javascript
// Функция удаления элемента
async function deleteItem(url, itemName) {
    // Спрашиваем подтверждение
    if (!confirm(`Вы уверены, что хотите удалить ${itemName}?`)) {
        return;
    }
    
    try {
        // Отправляем DELETE-запрос на сервер
        const response = await fetch(url, {
            method: 'DELETE',
            credentials: 'include'  // Отправляем cookies
        });
        
        if (response.ok) {
            location.reload();  // Перезагружаем страницу
        } else {
            alert('Ошибка при удалении');
        }
    } catch (error) {
        alert('Ошибка: ' + error.message);
    }
}

// Функция отправки формы
async function submitForm(formId, url, method = 'POST') {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();  // Отменяем стандартную отправку
        
        // Собираем данные из формы
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            // Преобразуем числовые поля
            if (key === 'amount' || key === 'target_amount') {
                data[key] = parseFloat(value);
            } else {
                data[key] = value;
            }
        });
        
        try {
            // Отправляем данные на сервер
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(data)  // Преобразуем в JSON
            });
            
            if (response.ok) {
                window.location.reload();
            } else {
                const error = await response.json();
                alert('Ошибка: ' + error.detail);
            }
        } catch (error) {
            alert('Ошибка: ' + error.message);
        }
    });
}

// Функция выхода из системы
async function logout() {
    const response = await fetch('/api/v1/auth/logout', {
        method: 'POST',
        credentials: 'include'
    });
    
    if (response.ok) {
        window.location.href = '/login';  // Переходим на страницу входа
    }
}
```

Что здесь происходит:
- `fetch()` — отправляет HTTP-запросы на сервер
- `async/await` — работа с асинхронным кодом (ждём ответа от сервера)
- `JSON.stringify()` — преобразует объект JavaScript в JSON-строку
- `credentials: 'include'` — отправляем cookies с запросом

---

### CSS-стили (style.css)

```css
/* Сброс стилей браузера */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Основные стили */
body {
    font-family: Arial, sans-serif;
    background: white;
    color: black;
    line-height: 1.5;
}

/* Контейнер для центрирования содержимого */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Навигационное меню */
.navbar {
    background: white;
    border-bottom: 1px solid black;
    padding: 15px 0;
}

/* Меню-список */
.nav-menu {
    display: flex;
    list-style: none;
    gap: 20px;
}

/* Кнопки */
.btn {
    padding: 8px 16px;
    border: 1px solid black;
    background: white;
    color: black;
    cursor: pointer;
}

.btn:hover {
    background: black;
    color: white;
}

/* Таблицы */
table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid black;
}

th, td {
    padding: 10px;
    text-align: left;
    border: 1px solid black;
}

thead {
    background: black;
    color: white;
}

/* Карточки статистики */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.stat-card {
    background: white;
    border: 1px solid black;
    padding: 15px;
}

/* Прогресс-бар */
.progress-bar {
    background: black;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}
```

Что здесь происходит:
- `box-sizing: border-box` — включаем padding и border в размер элемента
- `display: flex` — гибкое выравнивание элементов
- `display: grid` — сеточная раскладка
- `:hover` — стили при наведении мыши

---

## 6. СИСТЕМА БЕЗОПАСНОСТИ

### Как работает авторизация?

1. **Регистрация**: пользователь вводит email и пароль
2. **Хеширование пароля**: пароль шифруется (нельзя прочитать)
3. **JWT-токен**: создаётся "пропуск" для пользователя
4. **Cookie**: токен сохраняется в браузере
5. **Проверка**: при каждом запросе проверяется токен

### Шифрование паролей (crypt_module.py)

```python
import bcrypt

async def create_password_hash(password: str) -> bytes:
    """Создаёт хеш пароля (зашифрованную версию)"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

async def is_password_correct(password: str, passwordhash: bytes) -> bool:
    """Проверяет, правильный ли пароль"""
    return bcrypt.checkpw(password.encode(), passwordhash)
```

Что здесь происходит:
- `bcrypt` — библиотека для безопасного хеширования паролей
- `hashpw()` — создаёт хеш из пароля
- `gensalt()` — генерирует "соль" (случайные данные для усиления защиты)
- `checkpw()` — сравнивает пароль с хешем

**Почему не хранить пароли как есть?**
Если кто-то украдёт базу данных, он не сможет узнать пароли — только их хеши. А из хеша нельзя получить исходный пароль.

---

### JWT-токены

JWT (JSON Web Token) — это специальный "пропуск", который подтверждает личность пользователя.

```python
import jwt
import time

SECRET_TOKEN = "секретный-ключ"  # Известен только серверу

async def create_jwt_token(email: str) -> str:
    """Создаёт JWT-токен для пользователя"""
    payload = {
        "sub": email,              # Кто владелец токена
        "iss": "Finance_monitor",  # Кто выдал токен
        "iat": int(time.time()),   # Когда выдан
        "exp": int(time.time()) + 7 * 24 * 60 * 60  # Срок действия (7 дней)
    }
    token = jwt.encode(payload, SECRET_TOKEN, algorithm="HS256")
    return token

async def verify_jwt_token(token: str):
    """Проверяет JWT-токен"""
    try:
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

Что здесь происходит:
1. `payload` — данные, которые хранятся в токене
2. `jwt.encode()` — создаёт токен с подписью
3. `jwt.decode()` — расшифровывает и проверяет токен
4. Если токен просрочен или подделан — выдаём ошибку

---

### Проверка авторизации (dependencies.py)

```python
async def get_current_user_id(access_token: str = Cookie(None)) -> int:
    """Получить user_id из JWT токена из cookie"""
    if not access_token:
        raise HTTPException(status_code=401, detail="Authentication cookie missing")
    
    try:
        # Проверяем токен
        payload = await verify_jwt_token(access_token)
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Находим пользователя по email
        user = await get_user_info(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
```

Что здесь происходит:
1. `Cookie(None)` — получаем токен из cookie браузера
2. Проверяем, есть ли токен
3. Расшифровываем токен и получаем email
4. Находим пользователя в базе данных
5. Возвращаем ID пользователя

---

## 7. КАК РАБОТАЕТ ПРИЛОЖЕНИЕ

### Пошаговое описание работы

#### Сценарий 1: Регистрация нового пользователя

```
Пользователь                    Браузер                     Сервер                      База данных
    │                              │                           │                              │
    │  1. Заполняет форму          │                           │                              │
    │──────────────────────────────►                           │                              │
    │                              │                           │                              │
    │                              │ 2. POST /api/v1/auth/register                            │
    │                              │ {email, password, name}   │                              │
    │                              │──────────────────────────►│                              │
    │                              │                           │                              │
    │                              │                           │ 3. Хеширует пароль           │
    │                              │                           │                              │
    │                              │                           │ 4. INSERT INTO users         │
    │                              │                           │──────────────────────────────►
    │                              │                           │                              │
    │                              │                           │ 5. Создаёт JWT-токен         │
    │                              │                           │                              │
    │                              │ 6. Ответ + Cookie с токеном                              │
    │                              │◄──────────────────────────│                              │
    │                              │                           │                              │
    │  7. Перенаправление на /     │                           │                              │
    │◄──────────────────────────────                           │                              │
```

---

#### Сценарий 2: Добавление транзакции

```
Пользователь                    Браузер                     Сервер                      База данных
    │                              │                           │                              │
    │  1. Открывает /transactions  │                           │                              │
    │──────────────────────────────►                           │                              │
    │                              │                           │                              │
    │                              │ 2. GET /transactions      │                              │
    │                              │ + Cookie с токеном        │                              │
    │                              │──────────────────────────►│                              │
    │                              │                           │                              │
    │                              │                           │ 3. Проверяет токен           │
    │                              │                           │ 4. Получает user_id          │
    │                              │                           │                              │
    │                              │                           │ 5. SELECT FROM transactions  │
    │                              │                           │──────────────────────────────►
    │                              │                           │◄──────────────────────────────
    │                              │                           │                              │
    │                              │ 6. HTML-страница с данными│                              │
    │◄─────────────────────────────│◄──────────────────────────│                              │
    │                              │                           │                              │
    │  7. Заполняет форму          │                           │                              │
    │  8. Нажимает "Добавить"      │                           │                              │
    │──────────────────────────────►                           │                              │
    │                              │                           │                              │
    │                              │ 9. POST /api/v1/transaction/                             │
    │                              │ {amount, type, category_id, date}                        │
    │                              │──────────────────────────►│                              │
    │                              │                           │                              │
    │                              │                           │ 10. INSERT INTO transactions │
    │                              │                           │──────────────────────────────►
    │                              │                           │                              │
    │                              │ 11. Успех                 │                              │
    │                              │◄──────────────────────────│                              │
    │                              │                           │                              │
    │  12. Страница перезагружается│                           │                              │
    │◄──────────────────────────────                           │                              │
```

---

#### Сценарий 3: Добавление суммы к цели

```
Пользователь                    Браузер                     Сервер                      База данных
    │                              │                           │                              │
    │  1. Выбирает цель            │                           │                              │
    │  2. Вводит сумму: 1000       │                           │                              │
    │  3. Нажимает "Добавить"      │                           │                              │
    │──────────────────────────────►                           │                              │
    │                              │                           │                              │
    │                              │ 4. POST /api/v1/goal/5/add-amount?amount=1000            │
    │                              │──────────────────────────►│                              │
    │                              │                           │                              │
    │                              │                           │ 5. SELECT FROM goals WHERE id=5
    │                              │                           │──────────────────────────────►
    │                              │                           │◄──────────────────────────────
    │                              │                           │ current_amount = 5000        │
    │                              │                           │                              │
    │                              │                           │ 6. current_amount += 1000    │
    │                              │                           │    current_amount = 6000     │
    │                              │                           │                              │
    │                              │                           │ 7. if 6000 >= target_amount: │
    │                              │                           │       is_completed = True    │
    │                              │                           │                              │
    │                              │                           │ 8. UPDATE goals SET ...      │
    │                              │                           │──────────────────────────────►
    │                              │                           │                              │
    │                              │ 9. Успех                  │                              │
    │◄─────────────────────────────│◄──────────────────────────│                              │
```

---

## 8. ЗАПУСК ПРИЛОЖЕНИЯ

### Способ 1: Через Docker (рекомендуется)

Docker — это инструмент, который упаковывает приложение со всеми зависимостями в контейнер.

```bash
# 1. Создать файл .env с настройками
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=finances
SECRET_TOKEN=my-secret-token

# 2. Запустить приложение
docker-compose up --build
```

**Файл docker-compose.yml:**

```yaml
services:
  db:
    image: postgres:15          # База данных PostgreSQL
    environment:
      POSTGRES_DB: finances
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Сохраняем данные
    ports:
      - "5432:5432"

  backend:
    build: 
      context: .
      dockerfile: backend/Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/finances
      SECRET_TOKEN: secret-token
    ports:
      - "8000:8000"             # Приложение доступно на порту 8000
    depends_on:
      db:
        condition: service_healthy  # Ждём запуска базы данных

volumes:
  postgres_data:                # Том для сохранения данных базы
```

Что здесь происходит:
- `db` — контейнер с PostgreSQL
- `backend` — контейнер с нашим приложением
- `depends_on` — backend запускается только после запуска db
- `volumes` — данные базы сохраняются при перезапуске

---

### Способ 2: Локальный запуск

```bash
# 1. Создать виртуальное окружение
python -m venv venv

# 2. Активировать окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать файл .env

# 5. Запустить сервер
cd backend
python main.py
```

После запуска приложение доступно по адресу: http://localhost:8000

---

## ИТОГИ

### Что мы создали?

Полноценное веб-приложение для учёта личных финансов, которое включает:

1. **Систему пользователей** — регистрация, вход, безопасное хранение паролей
2. **Учёт транзакций** — запись доходов и расходов с категориями
3. **Бюджеты** — планирование расходов на период
4. **Цели** — накопление денег с отслеживанием прогресса
5. **Аналитику** — сводка по доходам, расходам и балансу

### Какие навыки применены?

- Программирование на Python
- Работа с базами данных (SQL, SQLAlchemy)
- Создание веб-приложений (FastAPI)
- Вёрстка веб-страниц (HTML, CSS)
- Программирование на JavaScript
- Работа с Docker
- Понимание принципов безопасности (хеширование, JWT)

### Что можно улучшить в будущем?

- Добавить графики расходов
- Сделать мобильную версию
- Добавить напоминания о платежах
- Интегрировать с банками
- Добавить семейный доступ
