import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers.predict import router


app = FastAPI(title="moderation api")
app.include_router(router)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": jsonable_encoder(exc.errors())},
    )


@app.exception_handler(Exception)
async def server_error_handler(request: Request, exc: Exception):
    logger.exception("prediction failed")
    return JSONResponse(
        status_code=500,
        content={"detail": "internal server error"},
    )
