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

    # Import models
    from app.models import user, product, cart_item, affiliate_source

    # Import and register Blueprints
    from app.routes import api_bp           # existing blueprint
    from app.routes.cart import cart_bp    # <-- import cart blueprint

    app.register_blueprint(api_bp)
    app.register_blueprint(cart_bp)        # <-- register cart blueprint

    # Root route
    @app.route("/")
    def index():
        return jsonify({"message": "Project backend is running!"})

    return app
