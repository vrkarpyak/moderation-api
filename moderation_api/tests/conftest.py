import pytest
from fastapi.testclient import TestClient

import repository
from main import app


@pytest.fixture
def item_data():
    return {
        "seller_id": 1,
        "is_verified_seller": False,
        "item_id": 10,
        "name": "велосипед",
        "description": "продаю велосипед",
        "category": 2,
        "images_qty": 1,
    }


@pytest.fixture
def client():
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_repository():
    repository.predictions.clear()
    yield
    repository.predictions.clear()
