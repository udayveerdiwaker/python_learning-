# ==============================================================================
# challenge.py - Product Catalog API Server
# ==============================================================================
# CHALLENGE: Complete the FastAPI routes to implement a Product Catalog API.
# Run the server using: uvicorn challenge:app --reload --port 8001
# Test it using your browser at: http://127.0.0.1:8001/docs

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="Product Catalog API",
    description="Challenge solution for the FastAPI Basics module.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# 1. Pydantic Validation Models
# ------------------------------------------------------------------------------
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, description="The name of the product")
    price: float = Field(..., gt=0, description="Product price (must be greater than 0)")
    quantity: int = Field(default=0, ge=0, description="Available stock quantity (must be 0 or more)")

class ProductResponse(ProductBase):
    id: int  # Extension model that includes ID for response objects

# 2. In-memory Product Database
products_db = [
    {"id": 1, "name": "Wireless Mouse", "price": 25.50, "quantity": 120},
    {"id": 2, "name": "Mechanical Keyboard", "price": 89.99, "quantity": 45},
    {"id": 3, "name": "UltraWide Monitor", "price": 349.99, "quantity": 15}
]

# ------------------------------------------------------------------------------
# 3. HTTP Endpoints
# ------------------------------------------------------------------------------

@app.get("/", tags=["General"])
def index():
    return {"message": "Welcome to the Product Catalog API. Go to /docs to test endpoints."}


@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
def get_products(min_price: Optional[float] = None):
    """
    READ (GET): Returns a list of all products.
    Allows optional filtering by 'min_price' (e.g. /products?min_price=50).
    """
    results = products_db
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]
    return results


@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product_by_id(product_id: int):
    """
    READ (GET): Retrieves a single product details by its database ID.
    Raises an HTTP 404 Exception if product_id is not found.
    """
    for p in products_db:
        if p["id"] == product_id:
            return p
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with ID {product_id} does not exist"
    )


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: ProductBase):
    """
    CREATE (POST): Creates a new product and appends it to the database list.
    Generates ID dynamically. Returns the created product.
    """
    # Generate new ID
    new_id = max(p["id"] for p in products_db) + 1 if products_db else 1
    
    # Convert Pydantic payload to dictionary and attach ID
    product_dict = product.model_dump()
    product_dict["id"] = new_id
    
    products_db.append(product_dict)
    return product_dict


@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK, tags=["Products"])
def delete_product(product_id: int):
    """
    DELETE: Removes a product from the database catalog by its ID.
    Raises an HTTP 404 Exception if the product is not found.
    """
    for index, p in enumerate(products_db):
        if p["id"] == product_id:
            removed = products_db.pop(index)
            return {"message": f"Product '{removed['name']}' deleted successfully"}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with ID {product_id} does not exist"
    )

# ------------------------------------------------------------------------------
# 🏆 Extension Challenges for You:
# 1. Add an UPDATE (PUT) endpoint at `/products/{product_id}` that accepts a Pydantic
#    model with optional fields, allowing users to modify the name, price, or quantity.
# 2. Add an inventory low-stock alert GET route `/products/low-stock` that returns all
#    products where `quantity` is less than 10.
# ------------------------------------------------------------------------------
