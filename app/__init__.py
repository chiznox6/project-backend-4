from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    CORS(app)

    # Import models (needed for migrations)
    from app.models import user, product, cart_item, affiliate_source

    # Import and register Blueprints
    from app.routes import api_bp           # central API blueprint (users, products, cart-items, affiliates)
    from app.routes.cart import cart_bp     # partner's extra cart blueprint

    app.register_blueprint(api_bp)          # /api/... endpoints
    app.register_blueprint(cart_bp)         # /cart/... endpoints

    # Root route
    @app.route("/")
    def index():
        return jsonify({"message": "Project backend is running!"})

    return app
