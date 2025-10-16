from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_recipe_empty_name():
    data = {
        "name": "",
        "ingredients": [{"name": "sugar", "amount": "10g"}],
        "total_time": 10,
        "description": "Bad recipe.",
    }
    r = client.post("/recipes", json=data)
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"


def test_create_recipe_too_long_name():
    data = {
        "name": "x" * 101,
        "ingredients": [{"name": "salt", "amount": "1g"}],
        "total_time": 10,
        "description": "Too long name.",
    }
    r = client.post("/recipes", json=data)
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"


def test_update_recipe_invalid_field_type():
    data = {
        "name": "Cake",
        "ingredients": [{"name": "flour", "amount": "100g"}],
        "total_time": 60,
        "description": "Sweet cake.",
    }
    client.post("/recipes", json=data)

    r = client.patch("/recipes/Cake", json={"total_time": "sixty"})
    print(r)
    assert r.status_code in (400, 422)
