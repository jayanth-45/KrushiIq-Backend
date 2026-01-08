from flask import Blueprint, request, current_app
from flasgger import swag_from
from utils.utils import success_response, error_response, validate_fields

farmer_bp = Blueprint('farmer', __name__)

@farmer_bp.route('/farmer-profile', methods=['GET'])
@swag_from({
    'tags': ['Farmer'],
    'parameters': [],
    'responses': {
        200: {
            'description': 'Farmer profile information',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'location': {'type': 'string'},
                            'land_acres': {'type': 'number'},
                            'language': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_profile():
    # Fetch from MongoDB (using a hardcoded email/id for demo purposes)
    profile = current_app.db.farmers.find_one({'name': 'John Doe'}, {'_id': 0})
    if not profile:
        profile = {
            'name': 'John Doe',
            'location': 'Bangalore, Karnataka',
            'land_acres': 2.5,
            'language': 'en'
        }
    return success_response(profile)

@farmer_bp.route('/farmer-profile', methods=['POST'])
@swag_from({
    'tags': ['Farmer'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'location': {'type': 'string'},
                    'land_acres': {'type': 'number'},
                    'language': {'type': 'string'}
                },
                'required': ['name', 'location', 'land_acres', 'language']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Confirmation of profile update',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def update_profile():
    data = request.get_json()
    
    # Simple validation
    is_valid, error_msg = validate_fields(['name', 'location', 'land_acres', 'language'], data)
    if not is_valid:
        return error_response(error_msg)

    # Upsert into MongoDB
    current_app.db.farmers.update_one(
        {'name': data['name']},
        {'$set': data},
        upsert=True
    )
    
    return success_response({'status': 'profile updated'})
