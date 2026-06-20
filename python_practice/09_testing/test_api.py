# test_api.py
# Run these tests in terminal: pytest test_api.py

from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

# 1. Create a simple mock FastAPI application to test against
app = FastAPI()

items_db = {
    "item_1": {"name": "Coding Keyboard", "price": 120.00},
    "item_2": {"name": "Ergonomic Mouse", "price": 65.50}
}

@app.get("/")
def read_root():
    return {"app": "Testing Demo", "status": "online"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return items_db[item_id]


# ------------------------------------------------------------------------------
# 2. TestClient Integration Tests
# ------------------------------------------------------------------------------
# Initialize the TestClient with our FastAPI app object
client = TestClient(app)

def test_read_root():
    """
    Test GET / route returns correct welcome message and 200 OK.
    """
    response = client.get("/")
    assert response.status_code == 200
    # response.json() automatically parses the response body from JSON to Python dict
    assert response.json() == {"app": "Testing Demo", "status": "online"}


def test_read_item_success():
    """
    Test GET /items/{item_id} returns correct product when matching item is found.
    """
    response = client.get("/items/item_1")
    assert response.status_code == 200
    assert response.json() == {"name": "Coding Keyboard", "price": 120.00}


def test_read_item_not_found():
    """
    Test GET /items/{item_id} returns a 404 status when item is missing.
    """
    response = client.get("/items/missing_item_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
