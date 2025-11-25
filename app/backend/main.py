import os

# from app.backend.routers import transaction_router, budget_router, category_router, goal_router, user_router
from routers.user_router import *
from routers.transaction_router import *
from routers.budget_router import *
from routers.goal_router import *
from routers.category_router import *

from database import *
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field, EmailStr, ConfigDict



app = FastAPI(title='finance-app', root_path='/api/v1')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(budget_router)
app.include_router(category_router)
app.include_router(goal_router)





if __name__ == "__main__":
    # import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)