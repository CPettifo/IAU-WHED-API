from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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
    api_key = request.headers.get('X-API-KEY')
    #if not is_valid_api_key(api_key):
    #    return jsonify({'error': 'Unauthorized'}), 401

    # param = request.args.get('param')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT OrgID, OrgName FROM whed_org;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

def is_valid_api_key(key):
    
    return key == "testkey123"

if __name__ == "__main__":
    app.run(debug=True)
