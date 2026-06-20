# models.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import Column, Integer, String, Decimal, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db_helper import Base

class DBProduct(Base):
    """
    SQLAlchemy Model mapping to the 'proj_products' MySQL table.
    """
    __tablename__ = "proj_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    price = Column(Decimal(10, 2), nullable=False)
    stock = Column(Integer, default=0)

class DBCartItem(Base):
    """
    SQLAlchemy Model mapping to the 'proj_cart_items' MySQL table.
    Stores temporary cart selections matched to a session_id.
    """
    __tablename__ = "proj_cart_items"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("proj_products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1)

    # Establish relationship to product details
    product = relationship("DBProduct")

class DBOrder(Base):
    """
    SQLAlchemy Model mapping to the 'proj_orders' MySQL table.
    """
    __tablename__ = "proj_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_email = Column(String(150), nullable=False)
    total_amount = Column(Decimal(10, 2), nullable=False)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, server_default=func.now())

    items = relationship("DBOrderItem", back_populates="order", cascade="all, delete-orphan")

class DBOrderItem(Base):
    """
    SQLAlchemy Model mapping to the 'proj_order_items' MySQL table.
    Stores historical price snapshots for checkout orders.
    """
    __tablename__ = "proj_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("proj_orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("proj_products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Decimal(10, 2), nullable=False)  # Price at the time of purchase

    order = relationship("DBOrder", back_populates="items")
    product = relationship("DBProduct")
