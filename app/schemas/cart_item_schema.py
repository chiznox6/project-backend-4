from app.models import CartItem
from app import ma

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True
        include_fk = True
        fields = ("id", "user_id", "product_id", "quantity", "notes", "added_at")
