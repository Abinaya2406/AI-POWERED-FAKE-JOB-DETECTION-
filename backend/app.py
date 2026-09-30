"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Flask Application Factory & Web Host
Author: Abinaya R
"""

import os
from flask import Flask, send_from_directory, jsonify

try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

from .routes import api_bp

def create_app():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(__name__, static_folder=root_dir)

    if HAS_CORS:
        CORS(app)

    @app.after_request
    def cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response

    # Register API blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(api_bp)  # Also expose /predict at root

    @app.route('/')
    def serve_index():
        frontend_html = os.path.join(root_dir, 'frontend.html')
        index_html = os.path.join(root_dir, 'index.html')
        if os.path.exists(frontend_html):
            return send_from_directory(root_dir, 'frontend.html')
        elif os.path.exists(index_html):
            return send_from_directory(root_dir, 'index.html')
        return jsonify({"message": "JobShield AI Backend Running"})

    @app.route('/<path:filename>')
    def serve_static(filename):
        target = os.path.join(root_dir, filename)
        if os.path.exists(target):
            return send_from_directory(root_dir, filename)
        return jsonify({"error": "Not found"}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print(f"\n[*] Backend server starting on http://127.0.0.1:{port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
