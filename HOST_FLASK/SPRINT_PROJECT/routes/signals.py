from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response

signals_bp = Blueprint('signals', __name__)

@signals_bp.route('/<int:signal_id>/state', methods=['PUT'])
def update_signal(signal_id):
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result
   
    data = request.json
    signal_state = data.get('signal_state')
       
    if not signal_state:
        return jsonify({'message': 'signal_state is required'}), 400
 
        # Step 2: Fetch data from database if token is valid
    try:
            # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
            # Query to fetch vehicle details
        query = f"update traffic_signals set signal_state = '{signal_state}' WHERE signal_id = {signal_id};"
        cursor.execute(query)
        conn.commit()
           
        query = f"select signal_state from traffic_signals WHERE signal_id = {signal_id};"
        cursor.execute(query)
        state = cursor.fetchone()
 
            # Check if vehicle exists
        if state:
            return jsonify({ "message": "Traffic signal updated",
                                 "signal_state": signal_state
                            }), 201
        else:
            return jsonify({
                    "status": 404,
                    "message": "signal id not found"
                }), 404
 
    except Exception as err:
        return jsonify({"status": 500, "message": "Database error", "error": str(err)}), 500
 
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@signals_bp.route('/<int:signal_id>', methods = ['DELETE'])
def deletesignal(signal_id):
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        #check if signal_id exists
        check_query= f"SELECT signal_id FROM traffic_signals WHERE signal_id={signal_id};"
        cursor.execute(check_query)
        data= cursor.fetchone()
            
        if not data:
            return jsonify({"status": 404, "message": "signal_id not found"}), 404
 
        query = f"DELETE FROM traffic_signals WHERE signal_id={signal_id};"
        cursor.execute(query)
        conn.commit()         
        return jsonify({"message":"Traffic signal deleted successfully"}), 200                
           
    except Exception as err:
        return jsonify({"status": 500, "message": "Database error", "error": str(err)}), 500
       
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()