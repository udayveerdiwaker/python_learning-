# main.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db_helper import get_db
import crud
import schemas

app = FastAPI(
    title="E-Commerce API Service",
    description="Project 5: Catalog stocks, guest sessions shopping carts, and transactional checkouts.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# Product Catalog Routes
# ------------------------------------------------------------------------------
@app.get("/products", response_model=List[schemas.ProductResponse], tags=["Products"])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.get("/products/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    return product


# ------------------------------------------------------------------------------
# Shopping Cart Routes
# ------------------------------------------------------------------------------
@app.get("/cart", response_model=List[schemas.CartItemResponse], tags=["Cart"])
def view_cart(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieves all items in the shopping cart for a specific guest session.
    """
    return crud.get_cart_items(db, session_id)


@app.post("/cart", response_model=schemas.CartItemResponse, tags=["Cart"])
def add_product_to_cart(session_id: str, item: schemas.CartItemAdd, db: Session = Depends(get_db)):
    """
    Adds a product to the cart. Checks if the product exists first.
    """
    product = crud.get_product_by_id(db, item.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product does not exist."
        )
        
    # Check if we have enough stock available before adding to cart
    if product.stock < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot add {item.quantity} items to cart. Only {product.stock} in stock."
        )
        
    return crud.add_to_cart(db, session_id, item)


# ------------------------------------------------------------------------------
# Checkout & Orders Routes
# ------------------------------------------------------------------------------
@app.post("/checkout", response_model=schemas.OrderResponse, tags=["Checkout"])
def checkout_cart(request: schemas.CheckoutRequest, db: Session = Depends(get_db)):
    """
    Checks out the items in the cart.
    Creates an order, deducts stock, and flushes the shopping cart.
    """
    try:
        order = crud.process_checkout(db, request.session_id, request.customer_email)
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/orders/{order_id}", response_model=schemas.OrderResponse, tags=["Checkout"])
def read_order_invoice(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )
    return order
