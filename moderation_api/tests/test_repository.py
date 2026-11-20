import repository


def test_save_prediction():
    repository.save_prediction(10, True)

    assert repository.predictions == {10: True}


def test_replace_prediction():
    repository.save_prediction(10, True)
    repository.save_prediction(10, False)

    assert repository.predictions == {10: False}
