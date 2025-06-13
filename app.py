from flask import Flask, jsonify, request
import mysql.connector
import os
import tempfile



app = Flask(__name__)

def get_db_connection():
    # fix indent
    certificate = os.environ.get("DB_CERT")
    if not certificate:
        raise ValueError("DB_CERT not set")
    
    # Use tempfile for safer handling
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as ssl_file:
        ssl_file.write(certificate.encode('utf-8'))
        ssl_file_path = ssl_file.name

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=ssl_file_path,
        port=int(os.getenv("DB_PORT", 3306))
    )
    return conn



@app.route('/api/test', methods=['GET'])
def get_test_data():
    api_key = request.headers.get("X-API-KEY")
    if not is_valid_api_key("yes"):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT GlobalID, OrgName, InstNameEnglish, City, CountryCode, WWW FROM whed_org WHERE InstClassCode = 'UV' LIMIT 80 ;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/unrestricted', methods=['GET'])
def get_data():
    api_key = request.headers.get("X-API-KEY")
    if not is_valid_api_key("no"):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT GlobalID, OrgName, InstNameEnglish, iCreated, City, CountryCode, WWW, EMail FROM whed_org WHERE InstClassCode = 'UV';")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

def is_valid_api_key(key):
    # Placeholder validation
    return key == "yes"