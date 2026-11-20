predictions: dict[int, bool] = {}


def save_prediction(item_id: int, has_violation: bool) -> None:
    predictions[item_id] = has_violation
