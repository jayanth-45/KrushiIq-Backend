import requests
from flask import Blueprint, request
from flasgger import swag_from
from utils.utils import success_response, error_response
from datetime import datetime, timedelta

weather_bp = Blueprint('weather', __name__)

# Geocoding and weather API endpoints
GEOCODING_URL = 'https://nominatim.openstreetmap.org/search'
WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast'


def get_coordinates(location):
    """Convert a location name to latitude and longitude."""
    try:
        response = requests.get(f'{GEOCODING_URL}?q={location}&format=json')
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return float(data['lat']), float(data['lon'])
        return None, None
    except Exception as e:
        return None, None

@weather_bp.route('/weather', methods=['GET'])
@swag_from({
    'tags': ['Weather'],
    'parameters': [
        {
            'name': 'location',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'City name (e.g., Bangalore)'
        }
    ],
    'responses': {
        200: {
            'description': 'Current weather data',
            'schema': {
                'type': 'object',
                'properties': {
                    'temperature': {'type': 'number'},
                    'humidity': {'type': 'number'},
                    'rainfall': {'type': 'number'},
                    'description': {'type': 'string'}
                }
            }
        }
    }
})
def get_weather():
    location = request.args.get('location')
    if not location:
        return error_response("Location parameter is required")

    lat, lon = get_coordinates(location)
    if not lat or not lon:
        return error_response(f"Could not find coordinates for {location}")

    try:
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': 'true'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            current = data.get('current_weather', {})
            result = {
                'temperature': current.get('temperature', 0),
                'humidity': current.get('relativehumidity_2m', 0), # Placeholder if not available
                'rainfall': current.get('rain', 0), # Placeholder if not available
                'description': current.get('weathercode', 'N/A')
            }
            return success_response(result)
        else:
            return error_response(data.get('reason', 'Failed to fetch weather data'))

    except Exception as e:
        return error_response(str(e))

@weather_bp.route('/weather-forecast', methods=['GET'])
@swag_from({
    'tags': ['Weather'],
    'parameters': [
        {
            'name': 'location',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'City name'
        }
    ],
    'responses': {
        200: {
            'description': '7-day weather forecast'
        }
    }
})
def get_forecast():
    location = request.args.get('location')
    if not location:
        return error_response("Location parameter is required")

    lat, lon = get_coordinates(location)
    if not lat or not lon:
        return error_response(f"Could not find coordinates for {location}")

    try:
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,precipitation_sum,relativehumidity_2m_mean',
            'timezone': 'auto',
            'forecast_days': 7
        }
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()

        if response.status_code == 200 and 'daily' in data:
            daily_data = data['daily']
            forecast = []
            for i in range(len(daily_data.get('time', []))):
                forecast.append({
                    'day': daily_data['time'][i],
                    'temperature': daily_data['temperature_2m_max'][i],
                    'humidity': daily_data.get('relativehumidity_2m_mean', [0]*7)[i],
                    'rainfall': daily_data['precipitation_sum'][i]
                })
            return success_response({'forecast': forecast})
        else:
            return error_response(data.get('reason', 'Failed to fetch forecast data'))

    except Exception as e:
        return error_response(str(e))