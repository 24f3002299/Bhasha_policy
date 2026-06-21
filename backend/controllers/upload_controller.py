import os
import uuid
from flask import jsonify
from werkzeug.utils import secure_filename

# --- 1. RAG Pipeline Imports ---
from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import chunk_text
from rag.embeddings import create_vector_db

from agents.analyze_agent import run_analyze_agent

UPLOAD_FOLDER = 'uploads'

def process_upload(file):
    """
    Controller Logic: Secures the file, saves it locally, and kicks off the RAG ingestion.
    """
    try:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)
        
        # ---------------------------------------------------------
        # 2. The RAG Pipeline
        # ---------------------------------------------------------
        print(f"Initiating RAG pipeline for {filename}...")
        
        documents = extract_text_from_pdf(filepath)
        chunks = chunk_text(documents)
        vectorstore = create_vector_db(chunks) 
        
        # ---------------------------------------------------------
        # 3. Dynamic UI Generation (Eager Loading)
        # ---------------------------------------------------------
        print("Extracting sample text for Analyze Agent...")
        # Grab the text from the first 5 chunks (plenty of info for summary & evidence)
        sample_text = "\n".join([chunk.page_content for chunk in chunks[:5]])
        
        # Run the agent to get the JSON dictionary
        ui_data = run_analyze_agent(sample_text)
        
        return jsonify({
            'status': 'success',
            'message': f'Policy document "{filename}" successfully processed and vectorized!',
            'filename': filename,          # Fixed variable typo
            'analysis': ui_data            # Injected dynamic payload
        }), 200
        
    except Exception as e:
        print(f"Error during upload processing: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to process upload: {str(e)}'
        }), 500