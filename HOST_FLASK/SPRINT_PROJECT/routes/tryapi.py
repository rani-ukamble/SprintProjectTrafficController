app.config['sk'] = os.getenv('sk')

jwt = JWTmanager(app)

@app.route('/signin', methods = ['POST'])
def signin():
    data = request.get_json()
    email=data.get('email')
    pass = data.get('pass')

    if not email or not pass:
        return jsonify({
            "message": "fields required"
        })
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select * from traffic where email=%s and pass=%s"""
        cursor.execute(query, (email, pass))

        user = cursor.fetchone()
        if not user:
            return jsonify({
                "status":400
            })
