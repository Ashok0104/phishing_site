from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from backend.analyzer import URLAnalyzer

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes

# Initialize the URL analyzer
analyzer = URLAnalyzer()

@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """
    Analyze a URL for potential phishing or vulnerabilities
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    try:
        # Perform the analysis
        result = analyzer.analyze(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quick-analyze', methods=['POST'])
def quick_analyze():
    """
    Perform a quick analysis with fewer checks
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    try:
        # Perform a quick analysis
        result = analyzer.quick_analyze(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """
    Serve the main index.html file
    """
    return app.send_static_file('index.html')

# Serve all static files
@app.route('/<path:path>')
def serve_static(path):
    """
    Serve static files
    """
    return app.send_static_file(path)

if __name__ == '__main__':
    # Create the backend directory if it doesn't exist
    os.makedirs('backend', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
