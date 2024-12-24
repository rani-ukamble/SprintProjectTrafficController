from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response

violations_bp = Blueprint('violations', __name__)

@violations_bp.route('/<int:violation_id>', methods=['GET'])
def violation_report(violation_id):
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result
   
    if not violation_id:
        return jsonify({'message': 'violation_id is required'}), 400
 
    # Step 2: Fetch data from database if token is valid
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
            # Query to fetch vehicle details
        query = f"select v.violation_id, ve.vehicle_number, v.violation_type, v.fine_amount from violations v join vehicles ve on ve.vehicle_id = v.vehicle_id where v.violation_id = {violation_id};"
        cursor.execute(query)
        data = cursor.fetchone()
 
            # Check if vehicle exists
        if data:
            return jsonify(data), 200
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

@violations_bp.route('/generate', methods=['POST'])
def report_generation():
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result
   
    data = request.json
    vehicle_id = data.get('vehicle_id')
    signal_id = data.get('signal_id')
    violation_type = data.get('violation_type')
    fine_amount = data.get('fine_amount')
 
    if not vehicle_id or not signal_id or not violation_type or not fine_amount:
        return jsonify({'message':'please insert mandatory data'}), 400
       
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary = True)
 
        query = """
            INSERT INTO violations (vehicle_id, signal_id, violation_type, fine_amount) 
            VALUES (%s, %s, %s, %s);
            """
        cursor.execute(query, (vehicle_id, signal_id, violation_type, fine_amount))
        conn.commit()

        # Fetch the most recently generated violation ID
        cursor.execute("SELECT LAST_INSERT_ID() AS violation_id;")
        result = cursor.fetchone()
 
        if result:
            return jsonify({
                    "message": "Violation report generated",
                    "violation_id": result['violation_id']
                    })
        else:
            return jsonify({
                    "message":"report generation Unsuccessful"
                }), 404
 
    except Exception as err:
        return jsonify({"status": 500, "message": "Database error", "error": str(err)}), 500
       
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()