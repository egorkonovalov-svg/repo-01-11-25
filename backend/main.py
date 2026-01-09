
# from src.backend.routers import transaction_router, budget_router, category_router, goal_router, user_router
import sys
import os
from contextlib import asynccontextmanager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers.goal_router import *
from routers.transaction_router import *
from routers.budget_router import *
from routers.category_router import *
from routers.user_router import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import date
from database import init_db, close_db
from dependencies import get_current_user_id
from crypt_module import verify_jwt_token
from services.user_service import get_user_info

# Импортируем все модели, чтобы они были зарегистрированы в Base.metadata
from models import user, transaction, budget, category, goal


@asynccontextmanager
async def lifespan(app):
    await init_db()
    yield
    await close_db()


# root_path используется для генерации URL в документации
# HTML роуты работают напрямую, API роуты имеют префикс из роутеров
app = FastAPI(title='finance-src', lifespan=lifespan, debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # allow_cookies=True,
)

# Настройка Jinja2 и статических файлов
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# В Docker frontend в /frontend/, локально в ../frontend
if os.path.exists("/frontend"):
    FRONTEND_DIR = "/frontend"
else:
    FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")

# Добавляем функции в контекст Jinja2
def get_current_date():
    return date.today().isoformat()

templates.env.globals['current_date'] = get_current_date

# Вспомогательная функция для проверки аутентификации
async def get_user_id_from_cookie(access_token: str = None) -> int:
    """Получить user_id из cookie без использования Depends"""
    if not access_token:
        raise HTTPException(status_code=401, detail="Authentication cookie missing")
    
    try:
        payload = await verify_jwt_token(access_token)
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await get_user_info(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(budget_router)
app.include_router(category_router)
app.include_router(goal_router)

# HTML роуты
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница со сводкой"""
    try:
        user_id = await get_user_id_from_cookie(request.cookies.get("access_token"))
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    from services.transaction_service import get_transactions_summary
    from services.goal_service import get_user_goals
    from services.budget_service import get_user_budgets
    
    summary = await get_transactions_summary(user_id, None, None)
    goals = await get_user_goals(user_id, None)
    budgets = await get_user_budgets(user_id, None, None)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "summary": summary,
        "goals": goals[:5],  # Показываем только 5 последних
        "budgets": budgets[:5]
    })

@app.get("/transactions", response_class=HTMLResponse)
async def transactions_page(request: Request):
    """Страница транзакций"""
    try:
        user_id = await get_user_id_from_cookie(request.cookies.get("access_token"))
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    from services.transaction_service import get_user_transactions
    from services.category_service import get_user_categories
    
    transactions = await get_user_transactions(user_id, None, None, None, None, 100, 0)
    categories = await get_user_categories(user_id, None)
    
    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "transactions": transactions,
        "categories": categories
    })

@app.get("/categories", response_class=HTMLResponse)
async def categories_page(request: Request):
    """Страница категорий"""
    try:
        user_id = await get_user_id_from_cookie(request.cookies.get("access_token"))
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    from services.category_service import get_user_categories
    
    categories = await get_user_categories(user_id, None)
    
    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": categories
    })

@app.get("/budgets", response_class=HTMLResponse)
async def budgets_page(request: Request):
    """Страница бюджетов"""
    try:
        user_id = await get_user_id_from_cookie(request.cookies.get("access_token"))
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    from services.budget_service import get_user_budgets
    from services.category_service import get_user_categories
    
    budgets = await get_user_budgets(user_id, None, None)
    categories = await get_user_categories(user_id, None)
    
    return templates.TemplateResponse("budgets.html", {
        "request": request,
        "budgets": budgets,
        "categories": categories
    })

@app.get("/goals", response_class=HTMLResponse)
async def goals_page(request: Request):
    """Страница целей"""
    try:
        user_id = await get_user_id_from_cookie(request.cookies.get("access_token"))
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    from services.goal_service import get_user_goals
    
    goals = await get_user_goals(user_id, None)
    
    return templates.TemplateResponse("goals.html", {
        "request": request,
        "goals": goals
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Страница входа"""
    try:
        # Проверяем, авторизован ли пользователь
        await get_user_id_from_cookie(request.cookies.get("access_token"))
        # Если авторизован, перенаправляем на главную
        return RedirectResponse(url="/", status_code=303)
    except:
        # Если не авторизован, показываем страницу входа
        return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Страница регистрации"""
    try:
        # Проверяем, авторизован ли пользователь
        await get_user_id_from_cookie(request.cookies.get("access_token"))
        # Если авторизован, перенаправляем на главную
        return RedirectResponse(url="/", status_code=303)
    except:
        # Если не авторизован, показываем страницу регистрации
        return templates.TemplateResponse("register.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)