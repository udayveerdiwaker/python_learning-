# crud.py
from sqlalchemy.orm import Session
from models import DBProduct, DBCartItem, DBOrder, DBOrderItem
from schemas import CartItemAdd
from typing import List

# ------------------------------------------------------------------------------
# Product Queries
# ------------------------------------------------------------------------------
def get_products(db: Session):
    return db.query(DBProduct).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(DBProduct).filter(DBProduct.id == product_id).first()


# ------------------------------------------------------------------------------
# Cart Management
# ------------------------------------------------------------------------------
def get_cart_items(db: Session, session_id: str) -> List[DBCartItem]:
    return db.query(DBCartItem).filter(DBCartItem.session_id == session_id).all()

def add_to_cart(db: Session, session_id: str, item: CartItemAdd):
    """
    Adds a product to the cart. If the product already exists in the cart for
    this session, we increment the quantity.
    """
    # Check if item already exists in this session's cart
    db_cart_item = db.query(DBCartItem).filter(
        DBCartItem.session_id == session_id,
        DBCartItem.product_id == item.product_id
    ).first()
    
    if db_cart_item:
        db_cart_item.quantity += item.quantity
    else:
        db_cart_item = DBCartItem(
            session_id=session_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_cart_item)
        
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def clear_cart(db: Session, session_id: str):
    db.query(DBCartItem).filter(DBCartItem.session_id == session_id).delete()
    db.commit()


# ------------------------------------------------------------------------------
# Checkout & Order Processing (Transaction)
# ------------------------------------------------------------------------------
def process_checkout(db: Session, session_id: str, customer_email: str):
    """
    Processes cart checkout as a database transaction:
    1. Fetches all cart items.
    2. Validates product stock availability.
    3. Deducts stock quantities from products.
    4. Computes order total cost.
    5. Creates Order and OrderLineItem historical records.
    6. Flushes the guest's cart.
    
    Returns the created DBOrder object, or raises ValueError if stock is insufficient.
    """
    cart_items = get_cart_items(db, session_id)
    if not cart_items:
        raise ValueError("Cart is empty.")
        
    total_amount = 0
    order_items_to_create = []
    
    # 1. Validate stocks and calculate total
    for item in cart_items:
        product = item.product
        if not product:
            raise ValueError(f"Product ID {item.product_id} no longer exists.")
            
        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for product '{product.name}'. Available: {product.stock}, Requested: {item.quantity}")
            
        item_total = product.price * item.quantity
        total_amount += item_total
        
        # Deduct stock
        product.stock -= item.quantity
        
        # Prepare OrderItem
        order_item = DBOrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )
        order_items_to_create.append(order_item)
        
    # 2. Create the master order
    db_order = DBOrder(
        customer_email=customer_email,
        total_amount=total_amount,
        status="Processing"
    )
    db.add(db_order)
    db.flush() # Allocates database ID to db_order
    
    # 3. Associate items and write to DB
    for order_item in order_items_to_create:
        order_item.order_id = db_order.id
        db.add(order_item)
        
    # 4. Clear the cart
    clear_cart(db, session_id)
    
    # 5. Commit the full transaction
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: int):
    return db.query(DBOrder).filter(DBOrder.id == order_id).first()
