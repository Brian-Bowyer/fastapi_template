from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class NotFoundError(Exception):
    """Exception raised when a model could not be found in the database."""


class AlreadyExistsError(Exception):
    """Exception raised when a model already exists in the database (preventing an operation)."""


async def handle_exception(
    request,
    exc,
    *,
    status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
    message: str = "",
    **kwargs,
) -> JSONResponse:
    """Handles all exceptions."""
    payload = dict(
        status=status_code,
        type=str(exc.__class__.__name__),
        endpoint=f"{request.method} {request.url}",
        message=message,
        extra=kwargs.get("extra", {k: kwargs[k] for k in kwargs}),
    )
    return JSONResponse(status_code=status_code, content=payload)


def init_exception_handlers(app) -> None:
    @app.exception_handler(AlreadyExistsError)
    async def handle_already_exists_error(request, exc):
        return await handle_exception(
            request,
            exc,
            status_code=HTTP_409_CONFLICT,
            message=str(exc),
        )

    @app.exception_handler(NotFoundError)
    async def handle_not_found_error(request, exc):
        return await handle_exception(
            request,
            exc,
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            message=str(exc),
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_custom_http_exception(request, exc):
        try:
            message = exc.detail.get("message")
        except AttributeError:
            # not a dict, so try a str
            message = str(exc.detail)

        return await handle_exception(
            request,
            exc,
            status_code=exc.status_code,
            message=message,
            detail=exc.detail,
        )

    @app.exception_handler(Exception)
    async def handle_fallback_exception(request: Request, exc: Exception) -> JSONResponse:
        return await handle_exception(request, exc)
