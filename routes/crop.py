from flask import Blueprint, request, current_app
from flasgger import swag_from
from utils.utils import success_response, error_response, validate_fields

crop_bp = Blueprint('crop', __name__)

@crop_bp.route('/crop-recommendation', methods=['POST'])
@swag_from({
    'tags': ['Crop'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'soil_n': {'type': 'number'},
                    'soil_p': {'type': 'number'},
                    'soil_k': {'type': 'number'},
                    'ph': {'type': 'number'},
                    'location': {'type': 'string'},
                    'season': {'type': 'string'}
                },
                'required': ['soil_n', 'soil_p', 'soil_k', 'ph', 'location', 'season']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Crop recommendation result',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'recommended_crops': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'confidence': {'type': 'number'}
                        }
                    }
                }
            }
        }
    }
})
def crop_recommendation():
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_fields(['soil_n', 'soil_p', 'soil_k', 'ph', 'location', 'season'], data)
    if not is_valid:
        return error_response(error_msg)

    # In a real app, call ML model here. For now, use placeholder.
    result = {
        'recommended_crops': ['Wheat', 'Rice'],
        'confidence': 0.87
    }
    
    # Store recommendation in DB
    current_app.db.recommendations.insert_one({
        'type': 'crop',
        'input': data,
        'output': result
    })

    return success_response(result)

@crop_bp.route('/yield-prediction', methods=['POST'])
@swag_from({
    'tags': ['Crop'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'crop': {'type': 'string'},
                    'area_acres': {'type': 'number'},
                    'location': {'type': 'string'}
                },
                'required': ['crop', 'area_acres', 'location']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Yield prediction result',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'estimated_yield': {'type': 'number'},
                            'unit': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def yield_prediction():
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_fields(['crop', 'area_acres', 'location'], data)
    if not is_valid:
        return error_response(error_msg)

    # Placeholder logic
    result = {'estimated_yield': 3.5, 'unit': 'tons_per_acre'}
    
    # Store prediction in DB
    current_app.db.predictions.insert_one({
        'type': 'yield',
        'input': data,
        'output': result
    })

    return success_response(result)
