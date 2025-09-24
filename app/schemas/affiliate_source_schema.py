from app.models import AffiliateSource
from app.schemas import ma  # keep consistent with schemas/__init__.py

class AffiliateSourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AffiliateSource
        load_instance = True
        fields = ("id", "name", "api_name", "base_url")
        ordered = True  # ensures consistent JSON output order
