from flask import Blueprint, request
from flasgger import swag_from
from utils.utils import success_response, error_response, validate_fields

market_bp = Blueprint('market', __name__)

@market_bp.route('/market-prices', methods=['GET'])
@swag_from({
    'tags': ['Market'],
    'parameters': [
        {
            'name': 'crop',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Crop name to fetch market price for'
        }
    ],
    'responses': {
        200: {
            'description': 'Current market price for the crop',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'crop': {'type': 'string'},
                            'price_per_quintal': {'type': 'number'},
                            'unit': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_market_price():
    crop = request.args.get('crop')
    if not crop:
        return error_response("Crop parameter is required")
        
    # Placeholder static price; replace with real data source
    result = {'crop': crop, 'price_per_quintal': 2500, 'unit': 'INR'}
    return success_response(result)

@market_bp.route('/profit-estimation', methods=['POST'])
@swag_from({
    'tags': ['Market'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'crop': {'type': 'string'},
                    'estimated_yield': {'type': 'number'},
                    'price_per_quintal': {'type': 'number'},
                    'cost_per_quintal': {'type': 'number'}
                },
                'required': ['crop', 'estimated_yield', 'price_per_quintal', 'cost_per_quintal']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Profit estimation result',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'estimated_profit': {'type': 'number'},
                            'currency': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def profit_estimation():
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_fields(['crop', 'estimated_yield', 'price_per_quintal', 'cost_per_quintal'], data)
    if not is_valid:
        return error_response(error_msg)

    profit = (data['price_per_quintal'] - data['cost_per_quintal']) * data['estimated_yield']
    result = {'estimated_profit': profit, 'currency': 'INR'}
    return success_response(result)
