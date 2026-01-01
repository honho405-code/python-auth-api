from flask import Flask, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# 连接 MongoDB
MONGO_URL = os.getenv("MONGO_URL")
if MONGO_URL:
    client = MongoClient(MONGO_URL)
    db = client.auth_db
else:
    client = None
    print("警告：MONGO_URL 未设置")

@app.route("/")
def home():
    return jsonify({"message": "Auth API is running!", "status": "OK"})

@app.route("/health")
def health():
    if client:
        try:
            client.admin.command('ping')
            db_status = "connected"
        except:
            db_status = "disconnected"
    else:
        db_status = "no_mongo_url"
    return jsonify({"status": "healthy", "database": db_status}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)