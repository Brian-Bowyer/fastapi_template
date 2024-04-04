from fastapi import FastAPI

from app.database import init_db
from app.routes.crud import router as crud_router
from app.routes.system import router as system_router
from app.utils.errors import init_exception_handlers
from app.utils.middleware import init_middleware

init_db()

app = FastAPI(
    # title=APP_TITLE,
    # description=APP_DESCRIPTION,
    # version=__version__,
)

app.include_router(system_router, tags=["system"])
app.include_router(crud_router, tags=["crud"])

init_exception_handlers(app)
init_middleware(app)
