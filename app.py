# app.py
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import psutil
import datetime
import time

app = Flask(__name__)
socketio = SocketIO(app)


def get_system_metrics():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent,
            "used": psutil.virtual_memory().used,
            "free": psutil.virtual_memory().free
        },
        "disk": {
            "percent": psutil.disk_usage('/').percent,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free
        }
    }

@app.route('/')
def index():
    return render_template('index.html')

def background_metrics():
    """Background task to emit metrics"""
    while True:
        metrics = get_system_metrics()
        socketio.emit('metrics', metrics)
        socketio.sleep(0.1)

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(background_metrics)

if __name__ == '__main__':
    print("Starting server... Open http://localhost:5000 in your browser")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)