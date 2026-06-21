# Start Flask
# Register Blueprints
# Run Server

import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.upload_route import upload_bp
from routes.query_routes import query_bp

def create_app():
    # Pure API Setup: No template_folder or static_folder needed!
    app = Flask(__name__)
    CORS(app)
    
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
    
    app.register_blueprint(upload_bp)
    app.register_blueprint(query_bp)
    
    # Simple Health Check Route
    @app.route('/')
    def index():
        return jsonify({"status": "online", "message": "BhashaPolicy AI API is running!"}), 200
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)