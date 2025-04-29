from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter, Gauge
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests', ['method', 'endpoint'])
RESPONSE_TIME = Gauge('app_response_time_seconds', 'Response time in seconds')

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return jsonify({"status": "ok", "message": "Welcome to the test application"})

@app.route('/api')
def api():
    REQUEST_COUNT.labels(method='GET', endpoint='/api').inc()
    return jsonify({"status": "ok", "message": "API endpoint"})

@app.route('/about')
def about():
    REQUEST_COUNT.labels(method='GET', endpoint='/about').inc()
    return jsonify({"status": "ok", "message": "About page"})

@app.route('/contact')
def contact():
    REQUEST_COUNT.labels(method='GET', endpoint='/contact').inc()
    return jsonify({"status": "ok", "message": "Contact page"})

if __name__ == '__main__':
    # Start Prometheus metrics server on port 8081
    start_http_server(8081)
    # Start Flask app on port 8080
    app.run(host='0.0.0.0', port=8080) 