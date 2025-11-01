from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field, EmailStr, ConfigDict
app = FastAPI(title="Workout app")

class UserSchema(BaseModel):
    # email: EmailStr какая-то проблема
    email: str
    username: str | None = Field(max_length=15)
    # password: str = Field(min_length=8) потом добавлю
    age: int = Field(ge=12, le=100)
    # model_config = ConfigDict(extra='forbid')

users = []


@app.post("/users")
def create_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "message":"user created"}


@app.get("/users")
def get_users():
    return users

if __name__ == "__main__":
    # import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)