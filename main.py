from fastapi import FastAPI

from src.exceptions import init_exception_handlers
# from src.middleware import init_middlewares
from src.models import init_db
from src.routes.auth import router as auth_router
from src.routes.note import router as note_router
from src.routes.user import router as user_router


app = FastAPI(title="Awesome Fast API Sandbox.")
app.include_router(auth_router)
app.include_router(note_router)
app.include_router(user_router)


@app.on_event("startup")
async def on_startup():
    init_exception_handlers(app)
    # init_middlewares(app)
    init_db()
