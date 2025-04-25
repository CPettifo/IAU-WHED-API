from flask import Flask, jsonify, request
import mysql.connector
import os
import tempfile



app = Flask(__name__)

headers = {
    'X-API-KEY': os.getenv("X-API-KEY")
}

def get_db_connection():
    certificate = os.environ.get("DB_CERT")
    if not certificate:
        raise ValueErorr("DB_CERT not set")
    
    ssl_file = "sa_cert.perm"
    with open(ssl_file, 'w') as ssl:
        ssl.write(certificate)

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=ssl_file
        # set default port to 3306 for API connections
        port=int(os.getenv("DB_PORT", 3306))
    )



@app.route('/api/data', methods=['GET'])
def get_data():
    api_key = os.getenv("API_KEY")
    if not is_valid_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    # param = request.args.get('param')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT OrgID, OrgName FROM whed_org LIMIT 20;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

def is_valid_api_key(key):
    return True
    #conn = get_db_connection()
    #cursor = conn.cursor()
    #cursor.execute("SELECT * FROM api_keys WHERE key_value = %s AND active = TRUE", (key,))
    #result = cursor.fetchone()
    #cursor.close()
    #conn.close()
    #return result is not None
