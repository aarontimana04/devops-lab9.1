import pytest
from fastapi.testclient import TestClient
from hello import add, app, greet

client = TestClient(app)


def test_greet_default():
    assert greet() == "Hello, World!"


def test_greet_custom():
    assert greet("Aaron") == "Hello, Aaron!"


@pytest.mark.parametrize("a,b,expected", [(2, 3, 5), (-1, 1, 0), (0, 0, 0)])
def test_add(a, b, expected):
    assert add(a, b) == expected


def test_hello_endpoint():
    response = client.get("/hello", params={"name": "Aaron"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Aaron!", "source": "FastAPI"}


def test_hello_default():
    assert client.get("/hello").json()["message"] == "Hello, World!"


def test_add_endpoint():
    response = client.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 5}


@pytest.mark.parametrize("query", ["a=x&b=3", "a=2"])
def test_add_validation(query):
    assert client.get(f"/add?{query}").status_code == 422
