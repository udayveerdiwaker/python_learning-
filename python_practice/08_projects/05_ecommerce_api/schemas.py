# schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int

    class Config:
        from_attributes = True

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)

class CartItemResponse(BaseModel):
    id: int
    session_id: str
    product_id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True

class CheckoutRequest(BaseModel):
    session_id: str
    customer_email: EmailStr

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    customer_email: str
    total_amount: Decimal
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
