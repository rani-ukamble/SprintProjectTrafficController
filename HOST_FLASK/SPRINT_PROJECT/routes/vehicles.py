from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('/register', methods=['POST'])
def register():
    validation_result = validate_response()
    if validation_result is not True:
        return validation_result

    data = request.json
    vehicle_number = data.get('vehicle_number')
    owner_name = data.get('owner_name')
    vehicle_type = data.get('vehicle_type')

    if not vehicle_number or not owner_name or not vehicle_type:
        return jsonify({'message': 'vehicle_number, owner_name, and vehicle_type are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type) VALUES (%s, %s, %s);"
        cursor.execute(query, (vehicle_number, owner_name, vehicle_type))
        conn.commit()

        vehicle_id = cursor.lastrowid
        return jsonify({"message": "Vehicle registered successfully", "vehicle_id": vehicle_id}), 201

    except Exception as err:
        return jsonify({"status": 500, "message": "Database error", "error": str(err)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@vehicles_bp.route('/<string:vehicle_id>', methods=['GET'])
def get_vehicle_details(vehicle_id):
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result

    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Query to fetch vehicle details
        query = f"SELECT * FROM vehicles WHERE vehicle_id = '{vehicle_id};'"
        cursor.execute(query)
        vehicle = cursor.fetchone()
 
        # Check if vehicle exists
        if vehicle:
            return jsonify(vehicle), 201
        else:
            return jsonify({
                    "status": 404,
                    "message": "Vehicle not found"
                }), 404
 
    except Exception as err:
        return jsonify({"status": 500, "message": "Database error", "error": str(err)}), 500
 
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
