from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from db_config import db_config

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return "Job Market API is Running! Go to /api/jobs to see data."

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # dictionary=True makes data easy to read (JSON-like)
        
        # Fetch all jobs, newest first
        query = "SELECT * FROM jobs ORDER BY id DESC"
        cursor.execute(query)
        jobs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(jobs)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)