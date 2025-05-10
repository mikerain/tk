from flask import Flask
import threading
import time
import logging

app = Flask(__name__)

# 配置日志
logging.basicConfig(filename='/var/log/flask/app.log', level=logging.INFO, format='%(asctime)s %(message)s')

def log_writer():
    while True:
        logging.info(f'Heartbeat log entry at {time.strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(1)

# 启动一个线程来写日志
threading.Thread(target=log_writer, daemon=True).start()

@app.route('/')
def home():
    return "Logging every second! Check app.log."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

