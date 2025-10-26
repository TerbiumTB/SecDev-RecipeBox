from fastapi.testclient import TestClient


def test_create_recipe_empty_name(client: TestClient):
    data = {
        "name": "",
        "ingredients": [{"name": "sugar", "amount": 10, "units": "g"}],
        "total_time": 10,
        "description": "Bad recipe.",
    }
    r = client.post("/recipes", json=data)
    assert r.status_code == 422
    assert r.json()["title"] == "Validation Error"
    assert r.json()["detail"] == "pydantic error"


def test_create_recipe_too_long_name(client: TestClient):
    data = {
        "name": "x" * 101,
        "ingredients": [{"name": "salt", "amount": 1, "units": "g"}],
        "total_time": 10,
        "description": "Too long name.",
    }
    r = client.post("/recipes", json=data)
    assert r.status_code == 422
    assert r.json()["title"] == "Validation Error"
    assert r.json()["detail"] == "pydantic error"


def test_update_recipe_invalid_field_type(client: TestClient):
    data = {
        "name": "Cake",
        "ingredients": [{"name": "flour", "amount": 100, "units": "g"}],
        "total_time": 60,
        "description": "Sweet cake.",
    }
    client.post("/recipes", json=data)

    r = client.patch("/recipes/Cake", json={"total_time": "sixty"})
    assert r.status_code in (400, 422)
