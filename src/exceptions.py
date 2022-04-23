from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette import status


class BadRequestException(Exception):
    pass


class DBException(Exception):
    pass


def init_exception_handlers(app: FastAPI):

    @app.exception_handler(DBException)
    def db_exception_handler(request: Request, exc: DBException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BadRequestException)
    def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )
