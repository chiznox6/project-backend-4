from app.models import User
from app.schemas import ma  # import from schemas/__init__.py to stay consistent

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        # Explicitly whitelist safe fields
        fields = ("id", "name", "email", "created_at")
        ordered = True  # ensures consistent JSON output order
