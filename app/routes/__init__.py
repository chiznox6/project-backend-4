# app/routes/__init__.py
from flask import Blueprint
from app.routes.main_routes import main_routes
from app.routes.users import user_bp

# Create a central Blueprint for registering all routes
api_bp = Blueprint("api", __name__)

# Register individual route Blueprints
api_bp.register_blueprint(main_routes)
api_bp.register_blueprint(user_bp)
