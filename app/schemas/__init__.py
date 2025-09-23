from flask_marshmallow import Marshmallow

ma = Marshmallow()

from .user_schema import UserSchema
from .affiliate_source_schema import AffiliateSourceSchema
from .product_schema import ProductSchema
from .cart_item_schema import CartItemSchema
