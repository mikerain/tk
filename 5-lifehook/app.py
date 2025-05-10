from flask import Flask, send_from_directory, render_template_string
import threading
import time
import logging
import os

app = Flask(__name__)

# 配置日志
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

startup_time = time.time()

def log_writer():
    while True:
        logging.info(f'Heartbeat log entry at {time.strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(1)

# 启动一个线程来写日志
threading.Thread(target=log_writer, daemon=True).start()

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Flask Logger</title></head>
    <body>
        <h1>Logging every second!</h1>
        <p>Check app.log</p>
        <button onclick="loadImage()">Show Image</button>
        <div id="image-container"></div>
        <script>
            function loadImage() {
                const img = document.createElement("img");
                img.src = "/image";
                img.style.maxWidth = "500px";
                document.getElementById("image-container").appendChild(img);
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/ready')
def readiness():
    if time.time() - startup_time < 120:
        time.sleep(120)
        return "Not Ready", 503
    return "OK", 200

@app.route('/image')
def get_image():
    return send_from_directory('static', 'sample.jpg')

if __name__ == "__main__":
    # 创建 static 目录并添加占位图片（仅用于演示）
    os.makedirs('static', exist_ok=True)
    if not os.path.exists('static/sample.jpg'):
        with open('static/sample.jpg', 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0' + b'0' * 1000 + b'\xff\xd9')  # 生成一个简单的 fake JPEG

    app.run(host="0.0.0.0", port=5000)

