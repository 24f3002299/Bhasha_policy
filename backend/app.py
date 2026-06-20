# Start Flask
# Register Blueprints
# Run Server

from flask import Flask, render_template
from routes.upload_route import upload_bp
# We will create query_routes.py soon, but let's keep it commented out 
# until the file exists so your server doesn't crash on startup.
from routes.query_routes import query_bp

def create_app():
    app = Flask(__name__)
    
    # Configure shared upload settings if needed
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
    
    # Register Blueprints
    app.register_blueprint(upload_bp)
    app.register_blueprint(query_bp)

    # --- THE FIX: Serve the Frontend UI ---
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )