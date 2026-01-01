from flask import Flask, jsonify
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# 尝试多种可能的环境变量名
MONGO_URL = os.getenv("MONGO_URL") or os.getenv("DATABASE_URL") or os.getenv("MONGODB_URL")

if MONGO_URL:
    try:
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        # 测试连接
        client.admin.command('ping')
        db = client.auth_db
        print("MongoDB 连接成功")
    except Exception as e:
        print(f"MongoDB 连接失败: {e}")
        client = None
else:
    client = None
    print("未找到 MongoDB 连接字符串")

@app.route("/")
def home():
    return jsonify({"message": "Auth API is running!", "status": "OK", "mongodb": "connected" if client else "not connected"})

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
    port = int(os.getenv("PORT", 8080))  # Railway 使用 8080
    app.run(host="0.0.0.0", port=port)