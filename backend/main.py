import os
from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import init_db, close_db
from dependencies import get_user_id_from_cookie
from routers.user_router import user_router
from routers.transaction_router import transaction_router
from routers.budget_router import budget_router
from routers.category_router import category_router
from routers.goal_router import goal_router
from services.transaction_service import get_user_transactions, get_transactions_summary
from services.category_service import get_user_categories
from services.budget_service import get_user_budgets
from services.goal_service import get_user_goals

import models  # noqa: F401 — register all models with Base.metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(title='finance-src', lifespan=lifespan, debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists("/frontend"):
    FRONTEND_DIR = "/frontend"
else:
    FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")

templates.env.globals['current_date'] = lambda: date.today().isoformat()


# --- Router registration ---

app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(budget_router)
app.include_router(category_router)
app.include_router(goal_router)


# --- Auth helper for HTML pages ---

async def _get_authenticated_user_id(request: Request) -> int | None:
    """Return user_id from the cookie, or None if not authenticated."""
    try:
        return await get_user_id_from_cookie(request.cookies.get("access_token"))
    except HTTPException:
        return None


async def _require_auth(request: Request) -> int | RedirectResponse:
    """Return user_id or a redirect to login if unauthenticated."""
    user_id = await _get_authenticated_user_id(request)
    if user_id is None:
        return RedirectResponse(url="/login", status_code=303)
    return user_id


# --- HTML routes ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    result = await _require_auth(request)
    if isinstance(result, RedirectResponse):
        return result
    user_id = result

    summary = await get_transactions_summary(user_id, None, None)
    goals = await get_user_goals(user_id, None)
    budgets = await get_user_budgets(user_id, None, None)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "summary": summary,
        "goals": goals[:5],
        "budgets": budgets[:5],
    })


@app.get("/transactions", response_class=HTMLResponse)
async def transactions_page(request: Request):
    result = await _require_auth(request)
    if isinstance(result, RedirectResponse):
        return result
    user_id = result

    transactions = await get_user_transactions(user_id, None, None, None, None, 100, 0)
    categories = await get_user_categories(user_id, None)

    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "transactions": transactions,
        "categories": categories,
    })


@app.get("/categories", response_class=HTMLResponse)
async def categories_page(request: Request):
    result = await _require_auth(request)
    if isinstance(result, RedirectResponse):
        return result
    user_id = result

    categories = await get_user_categories(user_id, None)

    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": categories,
    })


@app.get("/budgets", response_class=HTMLResponse)
async def budgets_page(request: Request):
    result = await _require_auth(request)
    if isinstance(result, RedirectResponse):
        return result
    user_id = result

    budgets = await get_user_budgets(user_id, None, None)
    categories = await get_user_categories(user_id, None)

    return templates.TemplateResponse("budgets.html", {
        "request": request,
        "budgets": budgets,
        "categories": categories,
    })


@app.get("/goals", response_class=HTMLResponse)
async def goals_page(request: Request):
    result = await _require_auth(request)
    if isinstance(result, RedirectResponse):
        return result
    user_id = result

    goals = await get_user_goals(user_id, None)

    return templates.TemplateResponse("goals.html", {
        "request": request,
        "goals": goals,
    })


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_id = await _get_authenticated_user_id(request)
    if user_id is not None:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user_id = await _get_authenticated_user_id(request)
    if user_id is not None:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
