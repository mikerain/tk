from flask import Flask
import threading
import time
import logging

app = Flask(__name__)

# 配置日志
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

# 用于控制 readiness 延迟
startup_time = time.time()

def log_writer():
    while True:
        logging.info(f'Heartbeat log entry at {time.strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(1)

# 启动一个线程来写日志
threading.Thread(target=log_writer, daemon=True).start()

@app.route('/')
def home():
    return "Logging every second! Check app.log."

@app.route('/ready')
def readiness():
    # 模拟前 60 秒不可用（阻塞或返回非 200）
    if time.time() - startup_time < 60:
        time.sleep(60)  # 可选：模拟超时
        return "Not Ready", 503
    return "OK", 200

@app.route('/notready')
def notreadiness():
    return "NOK", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

