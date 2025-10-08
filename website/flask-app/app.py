from flask import Flask, jsonify, request, render_template_string, render_template
import pickle
import base64
import os

app = Flask(__name__)

# Modern Shop Homepage
@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Essentials - Premium Tools & Services</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            color: #1a1a1a;
            line-height: 1.6;
            background: #fafafa;
        }
        
        nav {
            background: white;
            padding: 1.5rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: #2563eb;
            text-decoration: none;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }
        
        .nav-links a {
            color: #4b5563;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #2563eb;
        }
        
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5rem 2rem;
            text-align: center;
        }
        
        .hero-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 800;
        }
        
        .hero p {
            font-size: 1.25rem;
            opacity: 0.95;
            margin-bottom: 2rem;
        }
        
        .cta-button {
            background: white;
            color: #667eea;
            padding: 1rem 2.5rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .products-section {
            max-width: 1200px;
            margin: 4rem auto;
            padding: 0 2rem;
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .section-header h2 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }
        
        .section-header p {
            color: #6b7280;
            font-size: 1.1rem;
        }
        
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .product-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        
        .product-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        }
        
        .product-image {
            width: 100%;
            height: 300px;
            background: linear-gradient(135deg, #e0e7ff 0%, #f3f4f6 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            position: relative;
            overflow: hidden;
        }
        
        .product-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .placeholder-icon {
            color: #9ca3af;
        }
        
        .product-info {
            padding: 1.5rem;
        }
        
        .product-category {
            color: #667eea;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .product-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }
        
        .product-description {
            color: #6b7280;
            margin-bottom: 1rem;
            line-height: 1.6;
        }
        
        .product-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1.5rem;
        }
        
        .product-price {
            font-size: 1.75rem;
            font-weight: 700;
            color: #2563eb;
        }
        
        .add-to-cart {
            background: #2563eb;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .add-to-cart:hover {
            background: #1d4ed8;
        }
        
        footer {
            background: #1f2937;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
        }
        
        footer a {
            color: #60a5fa;
            text-decoration: none;
        }
        
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2rem;
            }
            
            .products-grid {
                grid-template-columns: 1fr;
            }
            
            .nav-links {
                gap: 1rem;
            }
        }
    </style>
</head>
<body>
    <nav>
        <div class="nav-content">
            <a href="/" class="logo">⚙️ DevOps Essentials</a>
            <ul class="nav-links">
                <li><a href="#products">Products</a></li>
                <li><a href="/info">API Info</a></li>
                <li><a href="#about">About</a></li>
            </ul>
        </div>
    </nav>
    
    <section class="hero">
        <div class="hero-content">
            <h1>Premium DevOps Tools</h1>
            <p>Elevate your infrastructure with our curated collection of essential DevOps products and services. Built for teams that ship fast.</p>
            <a href="#products" class="cta-button">Explore Products</a>
        </div>
    </section>
    
    <section class="products-section" id="products">
        <div class="section-header">
            <h2>Featured Products</h2>
            <p>Handpicked essentials for modern DevOps teams</p>
        </div>
        
        <div class="products-grid">
            <div class="product-card">
                <div class="product-image">
                    <span class="placeholder-icon">🐳</span>
                </div>
                <div class="product-info">
                    <div class="product-category">Containers</div>
                    <h3 class="product-title">Docker Premium</h3>
                    <p class="product-description">Enterprise-grade containerization platform with advanced orchestration capabilities and 24/7 support.</p>
                    <div class="product-footer">
                        <span class="product-price">$299</span>
                        <button class="add-to-cart">Add to Cart</button>
                    </div>
                </div>
            </div>
            
            <div class="product-card">
                <div class="product-image">
                    <span class="placeholder-icon">☸️</span>
                </div>
                <div class="product-info">
                    <div class="product-category">Orchestration</div>
                    <h3 class="product-title">Kubernetes Suite</h3>
                    <p class="product-description">Complete K8s management solution with automated scaling, monitoring, and seamless cluster deployment.</p>
                    <div class="product-footer">
                        <span class="product-price">$499</span>
                        <button class="add-to-cart">Add to Cart</button>
                    </div>
                </div>
            </div>
            
            <div class="product-card">
                <div class="product-image">
                    <span class="placeholder-icon">🚀</span>
                </div>
                <div class="product-info">
                    <div class="product-category">CI/CD</div>
                    <h3 class="product-title">Pipeline Pro</h3>
                    <p class="product-description">Lightning-fast CI/CD pipelines with intelligent caching, parallel execution, and zero-downtime deployments.</p>
                    <div class="product-footer">
                        <span class="product-price">$399</span>
                        <button class="add-to-cart">Add to Cart</button>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <footer>
        <p>&copy; 2025 DevOps Essentials. All rights reserved. | <a href="/info">API Documentation</a></p>
    </footer>
</body>
</html>
    ''')

# Vulnerable API endpoints (moved to /info route)
@app.route('/info')
def info_page():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>API Info - Vulnerable Endpoints</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1000px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #d32f2f; }
        .endpoint { background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 20px 0; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        a { color: #2563eb; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚠️ Vulnerable API Endpoints</h1>
        <p><a href="/">← Back to Shop</a></p>
        
        <div class="endpoint">
            <h3>POST /api/deserialize</h3>
            <p>Pickle deserialization vulnerability - allows arbitrary code execution</p>
        </div>
        
        <div class="endpoint">
            <h3>GET /api/greet?name=value</h3>
            <p>Server-Side Template Injection (SSTI) vulnerability</p>
        </div>
        
        <div class="endpoint">
            <h3>GET /api/info</h3>
            <p>Exposes version information and known vulnerabilities</p>
        </div>
        
        <div class="endpoint">
            <h3>GET /api/vulnerable-data</h3>
            <p>Returns sensitive configuration data without authentication</p>
        </div>
        
        <p style="margin-top: 30px;"><strong>Note:</strong> These endpoints are intentionally vulnerable for security testing and demonstration purposes.</p>
    </div>
</body>
</html>
    ''')

# Vulnerable endpoint using pickle (deserialization vulnerability)
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