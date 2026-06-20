# Receive PDF
# Pass PDF to controller

from flask import Blueprint, request, jsonify

# Import the controller logic (we will build this next)
from controllers.upload_controller import process_upload

# Define the blueprint
upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Route: /upload
    Method: POST
    Purpose: Receives the PDF from the user/frontend and passes it to the controller.
    """
    # 1. Basic Web-Layer Validation
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

    # 2. Handoff to Controller
    # The route's job is done. The controller handles the logic.
    return process_upload(file)