# challenge.py
# CHALLENGE: Complete the test functions at the bottom to test the functions and API routes.
# Run tests using: pytest challenge.py

import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import Optional

# ------------------------------------------------------------------------------
# 1. Functions & API to Test
# ------------------------------------------------------------------------------
def calculate_discounted_total(price: float, quantity: int, discount_code: Optional[str] = None) -> float:
    """
    Calculates total cost after applying discount codes.
    - If price < 0 or quantity <= 0, raises a ValueError.
    - Discount "SAVE10" -> deducts 10% from subtotal.
    - Discount "SAVE20" -> deducts 20% from subtotal.
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")
        
    subtotal = price * quantity
    
    if discount_code == "SAVE10":
        subtotal *= 0.90
    elif discount_code == "SAVE20":
        subtotal *= 0.80
        
    return round(subtotal, 2)


app = FastAPI()

class OrderRequest(BaseModel):
    price: float
    quantity: int
    discount_code: Optional[str] = None

@app.post("/order-total")
def get_order_total(order: OrderRequest):
    try:
        total = calculate_discounted_total(order.price, order.quantity, order.discount_code)
        return {"total": total}
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


# ------------------------------------------------------------------------------
# 2. CHALLENGE: Write Your Tests Below!
# ------------------------------------------------------------------------------
# Implement the assertions in each test block.

def test_calculate_total_no_discount():
    """
    Task: Test standard calculation without discount codes.
    E.g. price=10.0, quantity=3 -> total should be 30.0.
    """
    # Write your code below this line
    assert calculate_discounted_total(10.0, 3) == 30.0
    assert calculate_discounted_total(25.5, 2) == 51.0
    # Write your code above this line


def test_calculate_total_discounts():
    """
    Task: Test discount code applications.
    - price=100.0, qty=1, code="SAVE10" -> should be 90.0
    - price=100.0, qty=1, code="SAVE20" -> should be 80.0
    """
    # Write your code below this line
    assert calculate_discounted_total(100.0, 1, "SAVE10") == 90.0
    assert calculate_discounted_total(100.0, 1, "SAVE20") == 80.0
    # Write your code above this line


def test_calculate_total_errors():
    """
    Task: Test that invalid inputs raise ValueError.
    Use pytest.raises(ValueError) to assert exceptions.
    """
    # Write your code below this line
    # Example:
    # with pytest.raises(ValueError):
    #     calculate_discounted_total(-10, 5)
    
    with pytest.raises(ValueError) as excinfo:
        calculate_discounted_total(-5.0, 2)
    assert "Price cannot be negative" in str(excinfo.value)
    
    with pytest.raises(ValueError) as excinfo2:
        calculate_discounted_total(10.0, 0)
    assert "Quantity must be greater than zero" in str(excinfo2.value)
    # Write your code above this line


# TestClient for API endpoints
client = TestClient(app)

def test_api_success():
    """
    Task: Test POST /order-total with valid payload.
    Should return 200 OK and correct total.
    """
    # Write your code below this line
    payload = {"price": 50.0, "quantity": 2, "discount_code": "SAVE10"}
    response = client.post("/order-total", json=payload)
    assert response.status_code == 200
    assert response.json() == {"total": 90.0}
    # Write your code above this line


def test_api_bad_request():
    """
    Task: Test POST /order-total returns 400 Bad Request on negative price.
    """
    # Write your code below this line
    payload = {"price": -10.0, "quantity": 2}
    response = client.post("/order-total", json=payload)
    assert response.status_code == 400
    assert "Price cannot be negative" in response.json()["detail"]
    # Write your code above this line
