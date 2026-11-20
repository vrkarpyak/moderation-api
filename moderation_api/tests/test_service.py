from unittest.mock import Mock

import pytest

import repository
import services
from schemas import item_request


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
def test_predict(item_data, is_verified_seller, images_qty, expected):
    item_data["is_verified_seller"] = is_verified_seller
    item_data["images_qty"] = images_qty
    item = item_request(**item_data)

    result = services.predict(item)

    assert result is expected


def test_prediction_is_saved(item_data, monkeypatch):
    save_prediction = Mock()
    monkeypatch.setattr(repository, "save_prediction", save_prediction)
    item_data["images_qty"] = 0
    item = item_request(**item_data)

    result = services.predict(item)

    assert result is True
    save_prediction.assert_called_once_with(item.item_id, True)
