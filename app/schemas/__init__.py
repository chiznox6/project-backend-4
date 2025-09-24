from flask_marshmallow import Marshmallow

# Initialize Marshmallow instance
ma = Marshmallow()

# Import schemas after ma is defined
from .user_schema import UserSchema
from .affiliate_source_schema import AffiliateSourceSchema
from .product_schema import ProductSchema
from .cart_item_schema import CartItemSchema

# Export them for easier access
__all__ = [
    "ma",
    "UserSchema",
    "AffiliateSourceSchema",
    "ProductSchema",
    "CartItemSchema",
]
