from flask import Blueprint, request, jsonify

# Import the controller logic (we will build this next)
from controllers.query_controller import process_query

# Define the blueprint
query_bp = Blueprint('query_bp', __name__)

@query_bp.route('/ask', methods=['POST'])
def ask_agent():
    """
    Route: /ask
    Method: POST
    Purpose: Receives a JSON payload with the user's question and triggers the Agent pipeline.
    """
    # 1. Web-Layer Validation
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({
            'error': 'No query provided. Please send a JSON payload with a "query" key.'
        }), 400
        
    user_query = data['query'].strip()
    
    if not user_query:
        return jsonify({
            'error': 'The query cannot be empty.'
        }), 400

    # 2. Handoff to Controller
    # The web layer's job is done. The agents take over from here.
    return process_query(user_query)