from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    CORS(app)

    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app
