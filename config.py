import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Ensure DATABASE_URL uses correct format for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'ishop4u.db')}"
    )
    
    # Track modifications (keep as False for performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for Flask sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    
    # Optional: set environment
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
