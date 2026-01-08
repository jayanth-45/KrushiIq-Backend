import pytest
from app import app as flask_app
import mongomock

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/",
        "DB_NAME": "test_db"
    })
    
    # Mock MongoDB
    flask_app.db = mongomock.MongoClient().test_db
    
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
