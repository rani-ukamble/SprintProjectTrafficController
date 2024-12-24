from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response

sensors_bp = Blueprint('sensors', __name__)

@sensors_bp.route('/<int:sensor_id>/data', methods = ['GET'])
def sensor_data(sensor_id):
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result
   
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        query = f"select location, traffic_count, average_speed, traffic_condition from sensor_data where sensor_id = {sensor_id};"
        cursor.execute(query)
        data= cursor.fetchone()
 
        if data:
            return jsonify({"sensor_id": sensor_id,
                            "location": data['location'],
                            "traffic_count": data['traffic_count'],
                            "average_speed": data['average_speed'],
                            "traffic_condition": data['traffic_condition']
                            }), 201
           
        else:
            return jsonify({"status": 404,
                    "message": "fine_id not found"}), 404
           
    except Exception as err:
        return jsonify({"status": 500, "message": "Database error", "error": str(err)}), 500
       
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@sensors_bp.route('/<int:sensor_id>/adjust', methods=['PUT'])
def adjust_signals(sensor_id):
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result
   
    
    data = request.json
    traffic_condition = data.get('traffic_condition')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary = True)
 
        query = f"update sensor_data set traffic_condition= '{traffic_condition}' where sensor_id={sensor_id};"
        cursor.execute(query)
        conn.commit()
 
        query = f"select traffic_condition from sensor_data where sensor_id={sensor_id};"
        cursor.execute(query)
        data = cursor.fetchone()
 
        if data:
            return jsonify({
                "message": "Traffic Condition adjusted successfully",
                "traffic_condition": traffic_condition
                }), 200
 
        else:
            return jsonify({"message":"signal_id not found"}), 404
           
    except Exception as err:
        return jsonify({"status": 500, "message": "Database error", "error": str(err)}), 500
       
    finally:
        cursor.close()
        conn.close()