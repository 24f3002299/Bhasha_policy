import os
from groq import Groq
from langchain_community.vectorstores import Chroma
from rag.embeddings import get_embedding_model, DB_PATH
import chromadb

# Initialize the Groq client for fast expansion
# Make sure your GROQ_API_KEY environment variable is set
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def expand_query(original_query: str) -> str:
    """
    Uses Llama-3.3-70b via Groq to expand a specific user query 
    into broader medical and insurance parent categories.
    """
    prompt = f"""You are an insurance policy expert assistant. 
Your job is to expand the user's search query to include broader medical terms, parent categories, synonyms, or insurance classifications that the query falls under.

Examples:
- "Is knee replacement surgery covered?" -> Parent categories: Joint replacement, orthopedic surgery, major medical interventions.
- "I was injured while mountain climbing." -> Parent categories: Adventure sports, high-risk activities, extreme sports exclusions.
- "Does it cover bypass surgery?" -> Parent categories: Cardiac procedures, cardiovascular surgery, heart conditions.

User Query: "{original_query}"

Provide a concise list of the original query plus its broader parent categories and related medical terms. Do not write an essay, return only the expanded terms separated by spaces or commas.
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama3-3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1, # Keep it deterministic and focused
            max_tokens=100
        )
        expanded_terms = response.choices[0].message.content.strip()
        print(f"Original Query: {original_query}")
        print(f"Expanded Terms: {expanded_terms}")
        
        # Combine them so the retriever searches for both the specific and broad terms
        return f"{original_query} {expanded_terms}"
    except Exception as e:
        print(f"Query expansion failed: {e}. Falling back to original query.")
        return original_query


def retrieve_relevant_context(user_query: str, k: int = 15) -> str:
    """
    Expands the user query, searches ChromaDB, and returns a single unified context string.
    """
    # 1. Expand the query to capture parent-child relationships
    search_query = expand_query(user_query)
    
    # 2. Connect to the existing persistent database
    embeddings = get_embedding_model()
    client = chromadb.PersistentClient(path=DB_PATH)
    
    vectorstore = Chroma(
        client=client,
        embedding_function=embeddings
    )
    
    # 3. Perform the vector similarity search
    docs = vectorstore.similarity_search(search_query, k=k)
    
    # 4. Combine the retrieved document text chunks into a single block
    # Upgrade: Inject metadata (Page Numbers) directly into the prompt context
    context_chunks = []
    for doc in docs:
        # LangChain PDF loaders usually 0-index pages, so we add 1
        page_num = doc.metadata.get('page', 'Unknown')
        # if isinstance(page_num, int):
        #     page_num += 1 
            
        # Stamp the page number right above the text chunk!
        chunk_text = f"[Source: Page {page_num}]\n{doc.page_content}"
        context_chunks.append(chunk_text)
        
    context = "\n\n---\n\n".join(context_chunks)
    
    return context