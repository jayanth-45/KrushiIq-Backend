from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object('config.Config')

# Initialize MongoDB client
mongo_client = MongoClient(app.config['MONGO_URI'])
app.db = mongo_client[app.config['DB_NAME']]

# Register blueprints
from routes.weather import weather_bp
from routes.market import market_bp
from routes.farmer import farmer_bp
from routes.auth import auth_bp
from routes.ai_recommendations import ai_bp
from routes.crop import crop_bp # Keep for fertilizer recommendation

app.register_blueprint(weather_bp, url_prefix='/api')
app.register_blueprint(market_bp, url_prefix='/api')
app.register_blueprint(farmer_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')
app.register_blueprint(crop_bp, url_prefix='/api')


# Swagger configuration
swagger = Swagger(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
