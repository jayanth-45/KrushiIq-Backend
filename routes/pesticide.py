from flask import Blueprint, request, current_app
from flasgger import swag_from
from utils.utils import success_response, error_response, validate_fields

pesticide_bp = Blueprint('pesticide', __name__)

@pesticide_bp.route('/pesticide-recommendation', methods=['POST'])
@swag_from({
    'tags': ['Pesticide'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'disease': {'type': 'string'},
                    'crop': {'type': 'string'},
                    'area_acres': {'type': 'number'}
                },
                'required': ['disease', 'crop', 'area_acres']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Pesticide recommendation result',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'pesticide': {'type': 'string'},
                            'dosage_per_acre': {'type': 'number'},
                            'eco_friendly_alternative': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def pesticide_recommendation():
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_fields(['disease', 'crop', 'area_acres'], data)
    if not is_valid:
        return error_response(error_msg)

    # Placeholder logic – replace with actual recommendation engine
    result = {
        'pesticide': 'Cypermethrin',
        'dosage_per_acre': 0.5,
        'eco_friendly_alternative': 'Neem Oil'
    }
    
    # Store recommendation in DB
    current_app.db.pesticide_recommendations.insert_one({
        'input': data,
        'output': result
    })

    return success_response(result)
