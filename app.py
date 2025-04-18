from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

headers = {
    'X-API-KEY': os.getenv("X-API-KEY")
}

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )



@app.route('/api/data', methods=['GET'])
def get_data():
    api_key = 'testkey123'
    if not is_valid_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    # param = request.args.get('param')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT OrgID, OrgName FROM whed_org;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

def is_valid_api_key(key):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys WHERE key_value = %s AND active = TRUE", (key,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

if __name__ == "__main__":
    app.run(debug=True)
