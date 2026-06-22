import os
import shutil
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

# Define where the database will live on your server
DB_PATH = "vectorstore/insurance_db"

def get_embedding_model():
    """Initializes and returns the HuggingFace embedding model."""
    print("Loading HuggingFace Cloud Embeddings (Zero RAM footprint!)...")
    # Using the exact model from your notebook's vector DB creation step
    # return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    return HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        task="feature-extraction",
        huggingfacehub_api_token=os.environ.get("HF_TOKEN")
    )


def create_vector_db(clean_chunks):
    """
    Takes clean text chunks, generates embeddings, and stores them in ChromaDB.
    Clears the old database first to prevent duplicate entries during rapid hackathon testing.
    """
    print("Step 3: Preparing Vector Database...")
    
    # 1. Clear old database to prevent overlapping data during testing
    
    # if os.path.exists(DB_PATH):
    #     print("Removing old database...")
    #     shutil.rmtree(DB_PATH)
        
    # Ensure the directory structure exists
    os.makedirs(DB_PATH, exist_ok=True)
    
    # 2. Load the embedding model
    embeddings = get_embedding_model()
    
    # 3. Create the Persistent Client and Vectorstore
    print("Step 4: Creating new ChromaDB and generating embeddings...")
    client = chromadb.PersistentClient(path=DB_PATH)
    
    vectorstore = Chroma.from_documents(
        documents=clean_chunks,
        embedding=embeddings,
        client=client
    )
    
    print("✅ Vector DB Created Successfully!")
    return vectorstore