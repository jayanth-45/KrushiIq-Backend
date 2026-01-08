import os

class Config:
    """Application configuration loaded from environment variables."""
    # Flask settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')

    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME = os.getenv('DB_NAME', 'krushiiq_nova')

    # Swagger settings
    SWAGGER = {
        'title': 'KrushiIQ Nova API',
        'uiversion': 3,
        'openapi': '3.0.2'
    }
