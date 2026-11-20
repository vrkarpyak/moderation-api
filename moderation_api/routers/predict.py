from fastapi import APIRouter

import services
from schemas import item_request


router = APIRouter()


@router.post(
    "/predict",
    response_model=bool,
    responses={
        400: {"description": "invalid request"},
        500: {"description": "internal server error"},
    },
)
def predict(item: item_request) -> bool:
    return services.predict(item)
