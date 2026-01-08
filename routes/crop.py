from flask import Blueprint, request, current_app
from flasgger import swag_from
from utils.utils import success_response, error_response, validate_fields
import random

crop_bp = Blueprint('crop', __name__)

# Dummy data for crop recommendations
CROP_DATA = {
    "wheat": {"soil_n": 80, "soil_p": 40, "soil_k": 40, "ph": 6.5, "season": "rabi"},
    "rice": {"soil_n": 120, "soil_p": 60, "soil_k": 60, "ph": 6.0, "season": "kharif"},
    "maize": {"soil_n": 100, "soil_p": 50, "soil_k": 50, "ph": 6.2, "season": "kharif"},
    "cotton": {"soil_n": 150, "soil_p": 75, "soil_k": 75, "ph": 6.8, "season": "kharif"},
    "sugarcane": {"soil_n": 200, "soil_p": 100, "soil_k": 100, "ph": 7.0, "season": "perennial"},
}

# Dummy data for yield prediction
YIELD_DATA = {
    "wheat": {"base_yield": 3.0, "location_factor": {"north": 1.2, "south": 0.8, "east": 1.0, "west": 0.9}},
    "rice": {"base_yield": 4.0, "location_factor": {"north": 1.1, "south": 1.3, "east": 1.2, "west": 0.9}},
    "maize": {"base_yield": 2.5, "location_factor": {"north": 1.0, "south": 1.1, "east": 1.2, "west": 0.8}},
    "cotton": {"base_yield": 1.5, "location_factor": {"north": 0.9, "south": 1.2, "east": 1.0, "west": 1.1}},
    "sugarcane": {"base_yield": 80.0, "location_factor": {"north": 1.1, "south": 1.2, "east": 1.0, "west": 0.9}},
}

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

    # Simple recommendation logic based on dummy data
    recommended_crops = []
    for crop, conditions in CROP_DATA.items():
        score = 0
        if abs(data['soil_n'] - conditions['soil_n']) < 20:
            score += 1
        if abs(data['soil_p'] - conditions['soil_p']) < 10:
            score += 1
        if abs(data['soil_k'] - conditions['soil_k']) < 10:
            score += 1
        if abs(data['ph'] - conditions['ph']) < 0.5:
            score += 1
        if data['season'].lower() == conditions['season']:
            score += 1
        
        if score >= 3:
            recommended_crops.append(crop)

    if not recommended_crops:
        recommended_crops = [random.choice(list(CROP_DATA.keys()))]

    result = {
        'recommended_crops': recommended_crops,
        'confidence': round(random.uniform(0.7, 0.95), 2)
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

    crop = data['crop'].lower()
    location = data['location'].lower()

    if crop not in YIELD_DATA:
        return error_response(f"Yield data not available for crop: {data['crop']}")

    base_yield = YIELD_DATA[crop]["base_yield"]
    location_factor = YIELD_DATA[crop]["location_factor"].get(location, 1.0)
    
    estimated_yield = data['area_acres'] * base_yield * location_factor

    result = {'estimated_yield': round(estimated_yield, 2), 'unit': 'tons'}
    
    # Store prediction in DB
    current_app.db.predictions.insert_one({
        'type': 'yield',
        'input': data,
        'output': result
    })

    return success_response(result)
