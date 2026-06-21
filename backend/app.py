# Start Flask
# Register Blueprints
# Run Server

import os
from flask import Flask, render_template
from flask_cors import CORS
from routes.upload_route import upload_bp
from routes.query_routes import query_bp

def create_app():
    # 1. Point Flask to the new frontend folder (which is one level up and inside 'frontend')
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    
    app = Flask(__name__, 
                template_folder=frontend_dir,  # Where to find index.html
                static_folder=frontend_dir,    # Where to find style.css and script.js
                static_url_path='')            # Serve them at the root URL
    
    CORS(app)
    
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
    
    app.register_blueprint(upload_bp)
    app.register_blueprint(query_bp)
    
    # 2. Serve the real website!
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)