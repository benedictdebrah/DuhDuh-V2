from fastapi import FastAPI

from app.routers import users, blog
from app.core.config import settings
from app.database.models import create_db_and_tables



app = FastAPI(
    version= settings.API_V1_STR
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/", tags=["Homepage"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


app.include_router(users.UserRouter)
app.include_router(blog.PostRouter)

