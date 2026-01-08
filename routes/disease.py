from flask import Blueprint, request, current_app
from flasgger import swag_from
from utils.utils import success_response, error_response, validate_fields

disease_bp = Blueprint('disease', __name__)

@disease_bp.route('/disease-detection', methods=['POST'])
@swag_from({
    'tags': ['Disease'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'image_url': {'type': 'string'},
                    'crop': {'type': 'string'}
                },
                'required': ['image_url', 'crop']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Disease detection result',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'disease': {'type': 'string'},
                            'severity': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def disease_detection():
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_fields(['image_url', 'crop'], data)
    if not is_valid:
        return error_response(error_msg)

    # Placeholder logic – replace with actual model inference
    result = {'disease': 'Leaf Blight', 'severity': 'medium'}
    
    # Store detection in DB
    current_app.db.detections.insert_one({
        'type': 'disease',
        'input': data,
        'output': result
    })

    return success_response(result)
