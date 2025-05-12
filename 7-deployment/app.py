from flask import Flask, send_from_directory, render_template_string, request, jsonify
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
        <br><br>

        <label>CPU Load Duration (seconds):</label>
        <input type="number" id="duration" value="5" min="1" max="300">
        <button onclick="triggerLoad()">Trigger CPU Load</button>

        <div id="image-container"></div>
        <p id="status"></p>

        <script>
            function loadImage() {
                const img = document.createElement("img");
                img.src = "/image";
                img.style.maxWidth = "500px";
                document.getElementById("image-container").appendChild(img);
            }

            function triggerLoad() {
                const duration = document.getElementById("duration").value;
                fetch(`/load?duration=${duration}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("status").innerText = data.message;
                    });
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

@app.route('/load')
def high_cpu():
    try:
        duration = int(request.args.get("duration", 5))
        duration = max(1, min(duration, 600))  # 限制在 1~600 秒之间

        def cpu_stress():
            start = time.time()
            while time.time() - start < duration:
                [x**2 for x in range(1000000)]

        threading.Thread(target=cpu_stress).start()
        return jsonify({"message": f"✅ 正在模拟 CPU 压力 {duration} 秒..."})
    except Exception as e:
        return jsonify({"message": f"❌ 出错: {str(e)}"}), 400

if __name__ == "__main__":
    os.makedirs('static', exist_ok=True)
    if not os.path.exists('static/sample.jpg'):
        with open('static/sample.jpg', 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0' + b'0' * 1000 + b'\xff\xd9')

    app.run(host="0.0.0.0", port=5000)

