from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Service configurations - Updated URLs to match actual service paths
SERVICES = {
    'wazuh': {
        'name': 'Wazuh',
        'url': '/app/login',  # Wazuh redirects here
        'description': 'Security Monitoring',
        'icon': '🛡️'
    },
    'velociraptor': {
        'name': 'Velociraptor',
        'url': '/velociraptor/',
        'description': 'Endpoint Visibility',
        'icon': '🦖'
    },
    'shuffle': {
        'name': 'Shuffle',
        'url': '/shuffle/',
        'description': 'Security Automation',
        'icon': '🔄'
    },
    'iris': {
        'name': 'IRIS',
        'url': '/iris/',
        'description': 'Incident Response',
        'icon': '🔍'
    }
}

@app.route('/')
def index():
    return render_template('index.html', services=SERVICES)

@app.route('/api/services')
def get_services():
    return jsonify(SERVICES)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'services': list(SERVICES.keys())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)