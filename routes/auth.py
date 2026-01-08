from flask import Blueprint, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flasgger import swag_from
from utils.utils import success_response, error_response, validate_fields

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'email': {'type': 'string'}
                },
                'required': ['username', 'password', 'email']
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'User already exists or missing fields'}
    }
})
def register():
    data = request.get_json()
    is_valid, error_msg = validate_fields(['username', 'password', 'email'], data)
    if not is_valid:
        return error_response(error_msg)

    users = current_app.db.users
    if users.find_one({'email': data['email']}):
        return error_response("User already exists", 400)

    hashed_pw = generate_password_hash(data['password'])
    user_id = users.insert_one({
        'username': data['username'],
        'email': data['email'],
        'password': hashed_pw
    }).inserted_id

    return success_response({'status': 'User registered', 'user_id': str(user_id)}, 201)

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'}
                }
            }
        },
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    data = request.get_json()
    is_valid, error_msg = validate_fields(['email', 'password'], data)
    if not is_valid:
        return error_response(error_msg)

    users = current_app.db.users
    user = users.find_one({'email': data['email']})

    if not user or not check_password_hash(user['password'], data['password']):
        return error_response("Invalid credentials", 401)

    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return success_response({'token': token})
