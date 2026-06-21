import os
import google.generativeai as genai
from groq import Groq

# Setup clients
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_ai_model(prompt: str, json_mode: bool = False):
    """
    Tries Gemini first; if it hits quota or error, falls back to Groq.
    """
    # 1. Try Gemini
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        config = {'temperature': 0.0}
        if json_mode:
            config['response_mime_type'] = "application/json"
            
        response = model.generate_content(prompt, generation_config=config)
        return response.text.strip()
    
    except Exception as e:
        print(f"Gemini exhausted or failed: {e}. Falling back to Groq...")
        
        # 2. Fallback to Groq
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception as groq_e:
            print(f"Groq also failed: {groq_e}")
            raise Exception("All AI providers exhausted.")