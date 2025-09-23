from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .affiliate_source import AffiliateSource
from .product import Product
from .cart_item import CartItem
