import google.generativeai as genai
import io
import mimetypes
from flask import Blueprint, request, current_app
from flasgger import swag_from
from werkzeug.utils import secure_filename
from utils.utils import success_response, error_response, validate_fields

ai_bp = Blueprint('ai', __name__)

def configure_genai(vision=False):
    """Configure the generative AI model."""
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key':
        return None
    genai.configure(api_key=api_key)
    model_name = 'gemini-pro-vision' if vision else 'gemini-pro'
    return genai.GenerativeModel(model_name)

@ai_bp.route('/ai/crop-recommendation', methods=['POST'])
@swag_from({
    'tags': ['AI Recommendations'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'location': {'type': 'string',
                                 'description': 'The geographical location for the crop recommendation.'},
                    'month': {'type': 'string',
                              'description': 'The month for which the recommendation is sought.'}
                },
                'required': ['location', 'month']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'AI-powered crop recommendation.',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'recommendation': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input.'
        },
        503: {
            'description': 'AI service is unavailable.'
        }
    }
})
def get_crop_recommendation():
    """Generate a crop recommendation using the Gemini API."""
    model = configure_genai()
    if model is None:
        return error_response('AI service is not configured. Please set the GEMINI_API_KEY.', 503)

    data = request.get_json()
    is_valid, error_msg = validate_fields(['location', 'month'], data)
    if not is_valid:
        return error_response(error_msg)

    try:
        prompt = f"Recommend a suitable crop to grow in {data['location']} during the month of {data['month']}. Provide a short reason for your recommendation."
        response = model.generate_content(prompt)
        
        recommendation = response.text.strip()
        return success_response({'recommendation': recommendation})
    except Exception as e:
        return error_response(f'Failed to get AI recommendation: {e}', 500)


@ai_bp.route('/ai/disease-detection', methods=['POST'])
@swag_from({
    'tags': ['AI Recommendations'],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'image',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Image of the crop to be analyzed for diseases.'
        }
    ],
    'responses': {
        200: {
            'description': 'AI-powered disease detection.',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'detection_result': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input. Image file is required.'
        },
        503: {
            'description': 'AI service is unavailable.'
        }
    }
})
def detect_disease():
    """Detect crop disease from an image using the Gemini Pro Vision model."""
    model = configure_genai(vision=True)
    if model is None:
        return error_response('AI service is not configured. Please set the GEMINI_API_KEY.', 503)

    if 'image' not in request.files:
        return error_response('Image file is required.')

    image_file = request.files['image']
    if image_file.filename == '':
        return error_response('No selected file.')

    try:
        image_data = image_file.read()
        mimetype = image_file.mimetype or mimetypes.guess_type(image_file.filename)[0]

        if not mimetype or not mimetype.startswith('image'):
            return error_response('Invalid file type. Please upload an image.')

        image_parts = [
            {
                "mime_type": mimetype,
                "data": image_data
            },
        ]

        prompt_parts = [
            "Analyze the following image of a crop and identify any visible diseases. Provide the name of the disease and a brief description of the symptoms.",
            image_parts[0],
        ]

        response = model.generate_content(prompt_parts)
        detection_result = response.text.strip()

        return success_response({'detection_result': detection_result})
    except Exception as e:
        return error_response(f'Failed to process image: {e}', 500)

@ai_bp.route('/ai/pesticide-recommendation', methods=['POST'])
@swag_from({
    'tags': ['AI Recommendations'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'crop': {'type': 'string', 
                             'description': 'The type of crop affected.'},
                    'disease': {'type': 'string', 
                                'description': 'The disease identified in the crop.'}
                },
                'required': ['crop', 'disease']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'AI-powered pesticide recommendation.',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'recommendation': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input.'
        },
        503: {
            'description': 'AI service is unavailable.'
        }
    }
})
def get_pesticide_recommendation():
    """Generate a pesticide recommendation using the Gemini API."""
    model = configure_genai()
    if model is None:
        return error_response('AI service is not configured. Please set the GEMINI_API_KEY.', 503)

    data = request.get_json()
    is_valid, error_msg = validate_fields(['crop', 'disease'], data)
    if not is_valid:
        return error_response(error_msg)

    try:
        prompt = f"Recommend a pesticide for a {data['crop']} crop affected by {data['disease']}. Include the recommended dosage and an eco-friendly alternative if possible."
        response = model.generate_content(prompt)
        
        recommendation = response.text.strip()
        return success_response({'recommendation': recommendation})
    except Exception as e:
        return error_response(f'Failed to get AI recommendation: {e}', 500)