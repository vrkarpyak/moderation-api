from unittest.mock import Mock

import pytest

import repository
import services


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize(
    "is_verified_seller, images_qty, expected",
    [
        (True, 0, False),
        (True, 1, False),
        (True, 3, False),
        (False, 0, True),
        (False, 1, False),
        (False, 3, False),
    ],
)
def test_predict(client, item_data, is_verified_seller, images_qty, expected):
    item_data["is_verified_seller"] = is_verified_seller
    item_data["images_qty"] = images_qty

    response = client.post("/predict", json=item_data)

    assert response.status_code == 200
    assert response.json() is expected


@pytest.mark.parametrize(
    "field",
    [
        "seller_id",
        "is_verified_seller",
        "item_id",
        "name",
        "description",
        "category",
        "images_qty",
    ],
)
def test_missing_field(client, item_data, field):
    del item_data[field]

    response = client.post("/predict", json=item_data)

    assert response.status_code == 400
    assert isinstance(response.json()["detail"], list)


@pytest.mark.parametrize(
    "field",
    [
        "seller_id",
        "is_verified_seller",
        "item_id",
        "name",
        "description",
        "category",
        "images_qty",
    ],
)
def test_null_field(client, item_data, field):
    item_data[field] = None

    response = client.post("/predict", json=item_data)

    assert response.status_code == 400
    assert isinstance(response.json()["detail"], list)


@pytest.mark.parametrize(
    "field, value",
    [
        ("seller_id", "1"),
        ("is_verified_seller", "false"),
        ("is_verified_seller", 1),
        ("item_id", 1.5),
        ("item_id", True),
        ("name", 123),
        ("description", []),
        ("category", "2"),
        ("images_qty", 1.5),
    ],
)
def test_wrong_field_type(client, item_data, field, value):
    item_data[field] = value

    response = client.post("/predict", json=item_data)

    assert response.status_code == 400
    assert isinstance(response.json()["detail"], list)


@pytest.mark.parametrize(
    "field, value",
    [
        ("seller_id", 0),
        ("seller_id", -1),
        ("item_id", 0),
        ("item_id", -1),
        ("category", 0),
        ("category", -1),
        ("images_qty", -1),
        ("name", ""),
        ("name", "   "),
        ("description", ""),
        ("description", "   "),
    ],
)
def test_invalid_field_value(client, item_data, field, value):
    item_data[field] = value

    response = client.post("/predict", json=item_data)

    assert response.status_code == 400
    assert isinstance(response.json()["detail"], list)


def test_extra_field(client, item_data):
    item_data["price"] = 1000

    response = client.post("/predict", json=item_data)

    assert response.status_code == 400


def test_missing_body(client):
    response = client.post("/predict")

    assert response.status_code == 400


def test_invalid_json(client):
    response = client.post(
        "/predict",
        content="{bad json",
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400


def test_service_error(client, item_data, monkeypatch):
    monkeypatch.setattr(services, "predict", Mock(side_effect=RuntimeError("test error")))

    response = client.post("/predict", json=item_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "internal server error"}


def test_repository_error(client, item_data, monkeypatch):
    monkeypatch.setattr(
        repository, "save_prediction", Mock(side_effect=RuntimeError("test error"))
    )

    response = client.post("/predict", json=item_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "internal server error"}
