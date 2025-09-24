from app.models import Product
from app.schemas import ma  # keep consistent with schemas/__init__.py

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True
        fields = (
            "id",
            "name",
            "price",
            "image_url",
            "affiliate_link",
            "affiliate_source_id",
        )
        ordered = True  # ensures predictable JSON ordering
