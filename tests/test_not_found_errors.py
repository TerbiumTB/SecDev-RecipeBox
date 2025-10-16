from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_nonexistent_recipe():
    r = client.get("/recipes/NoSuchRecipe")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


def test_update_nonexistent_recipe():
    r = client.patch("/recipes/NoSuchRecipe", json={"description": "Does not exist."})
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


def test_delete_nonexistent_recipe():
    r = client.delete("/recipes/NoSuchRecipe")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"
