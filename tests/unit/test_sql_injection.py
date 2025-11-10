import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "injection",
    [
        "1; DROP TABLE recipes; --",
        "'; DROP TABLE ingredients; --",
        "' OR '1'='1",
        '" OR "1"="1" --',
    ],
)
def test_sql_injection_in_recipe_name_on_get(client: TestClient, injection: str):
    r = client.get(f"/recipes/{injection}")

    assert r.status_code in (400, 404)


def test_sql_injection_in_recipe_create(client: TestClient):
    data = {
        "name": "Neapolitano",
        "ingredients": [
            {"name": "spaghetti", "amount": 200, "units": "g"},
            {"name": "sauce", "amount": 100, "units": "g"},
        ],
        "total_time": 25,
        "description": "Classic Italian pasta.",
    }
    r = client.post("/recipes", json=data)

    injection_data = {
        "name": "'); DROP TABLE recipes; --",
        "description": "test injection",
        "total_time": 5,
        "ingredients": [{"name": "sugar", "amount": 10, "units": "g"}],
    }
    r = client.post("/recipes", json=injection_data)
    recipes = client.get("/recipes").json()

    assert r.status_code != 500
    assert len(recipes) == 2


def test_sql_injection_in_update_recipe(client: TestClient):
    malicious_name = "InjectedName'; DROP TABLE ingredients; --"
    r = client.patch(f"/recipes/{malicious_name}", json={"description": "update test"})

    assert r.status_code in (400, 404)


def test_sql_injection_in_query_params(client: TestClient):
    r = client.get("/recipes?name=' OR '1'='1")

    assert r.status_code in (200, 400)


def test_sql_injection_in_delete(client: TestClient):
    malicious_id = "1; DROP TABLE recipes; --"
    r = client.delete(f"/recipes/{malicious_id}")

    assert r.status_code in (400, 404)
