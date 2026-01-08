from flask import Blueprint, request
from flasgger import swag_from
from utils.utils import success_response, error_response

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather', methods=['GET'])
@swag_from({
    'tags': ['Weather'],
    'parameters': [
        {
            'name': 'location',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Location identifier (e.g., city name or coordinates)'
        }
    ],
    'responses': {
        200: {
            'description': 'Current weather data',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
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
        }
    }
})
def get_weather():
    location = request.args.get('location')
    if not location:
        return error_response("Location parameter is required")
        
    # Placeholder: return static data; replace with real API integration
    result = {
        'temperature': 28,
        'humidity': 70,
        'rainfall': 0,
        'description': 'Clear sky'
    }
    return success_response(result)

@weather_bp.route('/weather-forecast', methods=['GET'])
@swag_from({
    'tags': ['Weather'],
    'parameters': [
        {
            'name': 'location',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Location identifier'
        }
    ],
    'responses': {
        200: {
            'description': '7-day weather forecast',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'forecast': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'day': {'type': 'string'},
                                        'temperature': {'type': 'number'},
                                        'humidity': {'type': 'number'},
                                        'rainfall': {'type': 'number'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_forecast():
    location = request.args.get('location')
    if not location:
        return error_response("Location parameter is required")
        
    # Placeholder static forecast
    result = {
        'forecast': [
            {'day': 'Day 1', 'temperature': 28, 'humidity': 70, 'rainfall': 0},
            {'day': 'Day 2', 'temperature': 30, 'humidity': 65, 'rainfall': 0},
            {'day': 'Day 3', 'temperature': 27, 'humidity': 75, 'rainfall': 2},
            {'day': 'Day 4', 'temperature': 26, 'humidity': 80, 'rainfall': 5},
            {'day': 'Day 5', 'temperature': 29, 'humidity': 68, 'rainfall': 0},
            {'day': 'Day 6', 'temperature': 31, 'humidity': 60, 'rainfall': 0},
            {'day': 'Day 7', 'temperature': 28, 'humidity': 70, 'rainfall': 1}
        ]
    }
    return success_response(result)
