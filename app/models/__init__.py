from app.extensions import db

# Import models so they are registered with SQLAlchemy's metadata
from .user import User
from .affiliate_source import AffiliateSource
from .product import Product
from .cart_item import CartItem

__all__ = ["User", "AffiliateSource", "Product", "CartItem"]