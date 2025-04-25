from flask import Flask, jsonify, request
import mysql.connector
import os
import tempfile



app = Flask(__name__)

headers = {
    'X-API-KEY': os.getenv("X-API-KEY")
}

def get_db_connection():
    # Retrieve the cert from the environment variable
    db_cert_content = os.getenv("DB_CERT")
    ssl_ca_path = None

    # If the cert exists, write it to a temporary file
    if db_cert_content:
        # Create a temporary file for the cert
        temp_cert = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
        temp_cert.write(db_cert_content.encode('utf-8'))
        temp_cert.close()
        ssl_ca_path = temp_cert.name

    conn_params = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": int(os.getenv("DB_PORT", 3306)),
    }

    if ssl_ca_path:
        conn_params["ssl_ca"] = ssl_ca_path

    return mysql.connector.connect(**conn_params)



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
