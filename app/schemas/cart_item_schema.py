from app.extensions import ma
from app.models.cart_item import CartItem
from app.schemas.product_schema import ProductSchema

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    product = ma.Nested(ProductSchema)

    class Meta:
        model = CartItem
        include_fk = True

cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)