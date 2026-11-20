import repository
from schemas import item_request


def predict(item: item_request) -> bool:
    has_violation = not item.is_verified_seller and item.images_qty == 0
    repository.save_prediction(item.item_id, has_violation)
    return has_violation
