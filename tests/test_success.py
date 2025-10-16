from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_recipe_success():
    data = {
        "name": "Pasta",
        "ingredients": [
            {"name": "spaghetti", "amount": "200g"},
            {"name": "sauce", "amount": "100ml"},
        ],
        "total_time": 25,
        "description": "Classic Italian pasta.",
    }
    r = client.post("/recipes", json=data)
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Pasta"
    assert len(body["ingredients"]) == 2


def test_get_recipe_success():
    data = {
        "name": "Salad",
        "ingredients": [{"name": "lettuce", "amount": "1 head"}],
        "total_time": 5,
        "description": "Green and fresh.",
    }
    client.post("/recipes", json=data)
    r = client.get("/recipes/Salad")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Salad"
    assert body["description"] == "Green and fresh."


def test_update_recipe_success():
    data = {
        "name": "Soup",
        "ingredients": [{"name": "water", "amount": "1L"}],
        "total_time": 10,
        "description": "Simple soup.",
    }
    client.post("/recipes", json=data)

    update_data = {"description": "Hot tasty soup."}
    r = client.patch("/recipes/Soup", json=update_data)
    assert r.status_code == 200
    assert r.json()["description"] == "Hot tasty soup."


def test_delete_recipe_success():
    data = {
        "name": "Tea",
        "ingredients": [
            {"name": "water", "amount": "200ml"},
            {"name": "tea", "amount": "1 tsp"},
        ],
        "total_time": 3,
        "description": "Hot tea.",
    }
    client.post("/recipes", json=data)

    r = client.delete("/recipes/Tea")
    assert r.status_code == 204

    r2 = client.get("/recipes/Tea")
    assert r2.status_code == 404
