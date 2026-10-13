"""API del Laboratorio 9: funciones puras y rutas HTTP."""
from fastapi import FastAPI

app = FastAPI(title="Laboratorio 9 - FastAPI y Lambda")


def greet(name: str = "World") -> str:
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    return a + b


@app.get("/hello")
def hello_endpoint(name: str = "World"):
    return {"message": greet(name), "source": "FastAPI"}


@app.get("/add")
def add_endpoint(a: int, b: int):
    return {"result": add(a, b)}


if __name__ == "__main__":  # pragma: no cover - servidor interactivo
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
