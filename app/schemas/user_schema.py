from app.models import User
from app import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        fields = ("id", "name", "email", "created_at")
