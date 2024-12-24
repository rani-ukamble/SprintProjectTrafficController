from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response

fines_bp = Blueprint('fines', __name__)

@fines_bp.route('/<int:fine_id>/pay', methods = ['PUT'])
def update_fines(fine_id):
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the response
        return validation_result
   
    data = request.json
    date = data.get('payment_date')
 
    if not date:
        return jsonify({'message':'Date field is required'}), 400
       
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        query = f"update fines set fine_status = 'PAID', payment_date = %s where fine_id = %s;"
        cursor.execute(query,(date,fine_id))
        conn.commit()
 
        query = f"SELECT * FROM fines WHERE fine_id = {fine_id};"
        cursor.execute(query)
        result = cursor.fetchone()
 
        if result:
            return jsonify({
                "message":"Fine paid successfully",
                "fine_status": "Paid"
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



