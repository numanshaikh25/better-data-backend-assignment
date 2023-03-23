from fastapi import FastAPI
from database.db import init_db
from .routes.user_routes import router as user_router


app = FastAPI()


app.include_router(user_router, prefix="/api/users", tags=["users"])

@app.on_event("startup")
async def on_startup():
    await init_db()