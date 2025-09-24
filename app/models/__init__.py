from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance (bound later in app factory)
db = SQLAlchemy()

# Import models so they are registered with SQLAlchemy's metadata
from .user import User
from .affiliate_source import AffiliateSource
from .product import Product
from .cart_item import CartItem

__all__ = ["db", "User", "AffiliateSource", "Product", "CartItem"]
