import requests
from flask import request, jsonify

def validate_response():
    """
    Validates the Authorization token by calling the /validate endpoint.
    Returns 401 for missing token and 403 for invalid token.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.strip():
        return jsonify({
            "status": 401,
            "message": "Unauthorized: Authorization token is required"
        }), False

    parts = auth_header.split()
    if len(parts) != 2 or not parts[1].strip():
        return jsonify({
            "status": 401,
            "message": "Unauthorized: Authorization token cannot be empty"
        }), False

    validate_url = "http://127.0.0.1:2999/auth/validate"
    headers = {"Authorization": auth_header}
    response = requests.post(validate_url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return jsonify({
            "status": 403,
            "message": "Forbidden: Invalid Authorization token"
        }), False
