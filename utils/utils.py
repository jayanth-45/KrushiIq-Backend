# utils.py
"""Utility functions for the KrushiIQ Nova Flask backend.
Provides simple request validation and standardized JSON response helpers.
"""

from flask import jsonify

def success_response(data, status_code=200):
    """Return a Flask JSON response with a standard success envelope.
    Args:
        data (dict): Payload to include in the response.
        status_code (int): HTTP status code (default 200).
    Returns:
        Flask Response: JSON response with the given data.
    """
    return jsonify({"status": "success", "data": data}), status_code

def error_response(message, status_code=400):
    """Return a Flask JSON response for errors.
    Args:
        message (str): Human‑readable error description.
        status_code (int): HTTP status code (default 400).
    Returns:
        Flask Response: JSON error response.
    """
    return jsonify({"status": "error", "message": message}), status_code

def validate_fields(required_fields, payload):
    """Simple validation to ensure required fields are present.
    Args:
        required_fields (list): List of field names that must exist.
        payload (dict): JSON payload from the request.
    Returns:
        tuple: (bool, str) where bool indicates success, and str is an error message.
    """
    missing = [field for field in required_fields if field not in payload]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, ""
