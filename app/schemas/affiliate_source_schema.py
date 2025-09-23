from app.models import AffiliateSource
from app import ma

class AffiliateSourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AffiliateSource
        load_instance = True
        fields = ("id", "name", "api_name", "base_url")
