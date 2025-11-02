import os

from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field, EmailStr, ConfigDict
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from authx import AuthX, AuthXConfig

app = FastAPI(title="Workout app")

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["headers"]

security = AuthX(config=config)



class UserSchema(BaseModel):
    email: EmailStr
    username: str | None = Field(max_length=15)
    password: str = Field(min_length=8)
    age: int = Field(ge=12, le=100)
    # model_config = ConfigDict(extra='forbid')

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


users = []


@app.post("/users")
def create_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "message":"user created"}

@app.post("/login")
def login(credentials: UserLoginSchema):
    if credentials.email in users and credentials.password == credentials.password:
        token = security.create_access_token(uid=credentials.email)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/protected")
def protected():
    ...



if __name__ == "__main__":
    # import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)