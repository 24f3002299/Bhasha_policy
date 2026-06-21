from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_text(documents: list[Document]) -> list[Document]:
    """
    Splits loaded PDF documents into smaller, overlapping chunks.
    Filters out any empty chunks to keep the vector database clean.
    """
    print("Step 2: Slicing documents into chunks...")
    
    # Using the exact optimal parameters from your notebook
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )
    
    raw_chunks = text_splitter.split_documents(documents)
    
    # Clean the chunks (remove any that are just whitespace)
    clean_chunks = [
        chunk for chunk in raw_chunks
        if chunk.page_content.strip()
    ]
    
    print(f"Total valid chunks created: {len(clean_chunks)}")
    
    return clean_chunks