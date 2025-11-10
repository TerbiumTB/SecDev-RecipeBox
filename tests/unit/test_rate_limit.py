from fastapi.testclient import TestClient
import pytest

@pytest.mark.ratelimit
def test_get_recipes_rate_limit_exceed(client: TestClient):
    for _ in range(5): 
        r = client.get("/recipes")
        assert r.status_code != 429

    r = client.get("/recipes")
    assert r.status_code == 429


@pytest.mark.ratelimit
def test_get_recipe_rate_limit_exceed(client: TestClient):
    for _ in range(5): 
        r = client.get("/recipes/SomeRecipe")
        assert r.status_code != 429

    r = client.get("/recipes/SomeRecipe")
    assert r.status_code == 429



@pytest.mark.ratelimit
def test_create_recipe_rate_limit_exceed(client: TestClient):
    data = {
        "name": "Neapolitano",
        "ingredients": [
            {"name": "spaghetti", "amount": 200, "units": "g"},
            {"name": "sauce", "amount": 100, "units": "g"},
        ],
        "total_time": 25,
        "description": "Classic Italian pasta.",
    }

    for i in range(5): 
        data["name"] = f"Neopolitano{i}"
        r = client.post("/recipes", json=data)
        assert r.status_code != 429

    r = client.post("/recipes", json=data)
    assert r.status_code == 429

@pytest.mark.ratelimit
def test_update_recipe_rate_limit_exceed(client: TestClient):
    data = {
        "name": "Soup",
        "ingredients": [{"name": "water", "amount": 1, "units": "L"}],
        "total_time": 10,
        "description": "Simple soup.",
    }
    client.post("/recipes", json=data)

    update_data = {"description": "Hot tasty soup."}

    for i in range(5): 
        r = client.patch("/recipes/Soup", json=update_data)
        assert r.status_code != 429

    r = client.patch("/recipes/Soup", json=update_data)
    assert r.status_code == 429

@pytest.mark.ratelimit
def test_update_recipe_rate_limit_exceed(client: TestClient):
    data = {
        "name": "Tea",
        "ingredients": [
            {"name": "water", "amount": 200, "units": "ml"},
            {"name": "tea", "amount": 1, "units": "tsp"},
        ],
        "total_time": 3,
        "description": "Hot tea.",
    }
    client.post("/recipes", json=data)

    for i in range(5): 
        r = client.delete("/recipes/Tea")
        assert r.status_code != 429

    r = client.delete("/recipes/Tea")
    assert r.status_code == 429
