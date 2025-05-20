from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import time
import logging
import os
import sys
import configparser
import mysql.connector

app = Flask(__name__)

# 日志配置：输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    stream=sys.stdout
)

startup_time = time.time()

# 读取数据库配置
#config = configparser.ConfigParser()
#config.read('config/config.ini')
#db_config = {
#    "host": config.get("mysql", "host"),
#    "port": config.getint("mysql", "port"),
#    "user": config.get("mysql", "user"),
#    "password": config.get("mysql", "password"),
#    "database": config.get("mysql", "database")
#}

def load_db_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {
        'host': config.get('mysql', 'host'),
        'port': config.getint('mysql', 'port'),
        'user': config.get('mysql', 'user'),
        'password': config.get('mysql', 'password'),
        'database': config.get('mysql', 'database')
    }

# 写日志线程
def log_writer():
    while True:
        logging.info(f'Heartbeat log entry at {time.strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(1)

#threading.Thread(target=log_writer, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ready")
def readiness():
    if time.time() - startup_time < 120:
        time.sleep(120)
        return "Not Ready", 503
    return "OK", 200

@app.route("/image")
def get_image():
    return send_from_directory("static", "sample.jpg")

@app.route("/load")
def high_cpu():
    try:
        duration = int(request.args.get("duration", 5))
        duration = max(1, min(duration, 600))

        def cpu_stress():
            start = time.time()
            while time.time() - start < duration:
                [x**2 for x in range(1000000)]

        threading.Thread(target=cpu_stress).start()
        return jsonify({"message": f"✅ 正在模拟 CPU 压力 {duration} 秒..."})
    except Exception as e:
        return jsonify({"message": f"❌ 出错: {str(e)}"}), 400

@app.route("/query")
def query_table():
    db_config = load_db_config()
    try:
        conn = mysql.connector.connect(**db_config)
    except mysql.connector.Error as conn_err:
        logging.error(f"❌ 无法连接到数据库: {conn_err}")
        return jsonify({
            "error": "❌ 无法连接到数据库",
            "details": str(conn_err)
        }), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT host,user FROM user LIMIT 10")
        rows = cursor.fetchall()
        columns = ["host","user"]
        cursor.close()
        conn.close()
        return jsonify({"columns": columns, "rows": rows})
    except mysql.connector.Error as query_err:
        conn.close()
        return jsonify({
            "error": "❌ 查询数据库时出错",
            "details": str(query_err)
        }), 500


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    if not os.path.exists("static/sample.jpg"):
        with open("static/sample.jpg", "wb") as f:
            f.write(b'\xff\xd8\xff\xe0' + b'0' * 1000 + b'\xff\xd9')
    app.run(host="0.0.0.0", port=5000)

