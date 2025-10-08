from flask import Flask, jsonify, request, render_template_string
import pickle
import base64
import os

app = Flask(__name__)

# Vulnerable endpoint using pickle (deserialization vulnerability)
# Updates
@app.route('/api/deserialize', methods=['POST'])
def deserialize_data():
    """
    Vulnerable endpoint demonstrating pickle deserialization
    CVE associated with untrusted pickle data
    """
    try:
        data = request.json.get('data', '')
        decoded = base64.b64decode(data)
        result = pickle.loads(decoded)  # VULNERABLE: Arbitrary code execution
        return jsonify({'success': True, 'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint with version info
@app.route('/api/info')
def api_info():
    import flask
    import werkzeug
    import jinja2
    
    return jsonify({
        'service': 'Flask API Demo',
        'flask_version': flask.__version__,
        'werkzeug_version': werkzeug.__version__,
        'jinja2_version': jinja2.__version__,
        'python_version': os.sys.version,
        'vulnerabilities': {
            'flask': 'Using Flask 1.1.1 (released 2019) - Multiple security issues',
            'werkzeug': 'Using Werkzeug 0.16.0 - Known vulnerabilities',
            'jinja2': 'Using Jinja2 2.10.1 - Security patches missing',
            'note': 'These are intentionally outdated for security scanning demos'
        }
    })

# Test endpoint that demonstrates SSTI vulnerability
@app.route('/api/greet')
def greet():
    """
    Vulnerable to Server-Side Template Injection (SSTI)
    """
    name = request.args.get('name', 'World')
    # VULNERABLE: Direct template rendering from user input
    template = f'<h1>Hello {name}!</h1>'
    return render_template_string(template)

# Health check endpoint
@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'flask-api'})

# Vulnerable data endpoint
@app.route('/api/vulnerable-data')
def vulnerable_data():
    """
    Returns sample data with intentional security issues
    """
    return jsonify({
        'warning': 'This endpoint demonstrates common security issues',
        'issues': [
            'Exposing sensitive configuration data',
            'No authentication required',
            'Verbose error messages',
            'Using outdated dependencies'
        ],
        'dependencies': {
            'flask': '1.1.1 (CVE-2023-30861)',
            'werkzeug': '0.16.0 (CVE-2023-25577)',
            'jinja2': '2.10.1 (CVE-2020-28493)'
        }
    })

if __name__ == '__main__':
    # Running in debug mode (insecure for production)
    app.run(host='0.0.0.0', port=5000, debug=True)
