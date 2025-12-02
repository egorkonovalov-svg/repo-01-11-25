
# from src.backend.routers import transaction_router, budget_router, category_router, goal_router, user_router
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers.goal_router import *
from routers.transaction_router import *
from routers.budget_router import *
from routers.category_router import *
from routers.user_router import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

app = FastAPI(title='finance-src', root_path='/api/v1')
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