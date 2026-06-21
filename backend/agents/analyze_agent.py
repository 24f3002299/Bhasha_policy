import os
import json
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_analyze_agent(document_text: str) -> dict:
    """
    Scans the beginning of the document to extract metadata and generate initial evidence cards.
    """
    print("Running Analyze Agent (Eager Loading UI)...")
    
    prompt = f"""You are a strict JSON data-extraction agent for BhashaPolicy.
Analyze the following extracted text from an insurance policy document.
Return EXACTLY a valid JSON object. Do not output any conversational text or markdown formatting outside the JSON block.

TEXT TO ANALYZE:
{document_text[:6000]}  # We only need the first ~6000 characters to find this info

REQUIRED JSON FORMAT:
{{
  "policyName": "Extract the exact name of the policy",
  "insurer": "Extract the insurance company name",
  "policyType": "Classify as Health, Term Life, Motor, or Other",
  "premium": "Extract if found, else write 'Not specified'",
  "sumInsured": "Extract if found, else write 'Not specified'",
  "summary": "Write a 2-3 sentence plain language summary of the policy.",
  "evidenceCards": [
    {{
      "type": "covered", 
      "title": "Example Coverage",
      "text": "Short description of what is covered.",
      "clause": "Clause X.Y",
      "page": 1
    }}
    // Generate exactly 4 cards total. Mix types: 'covered', 'excluded', 'limit', or 'condition'.
  ]
}}
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1, # Keep it highly factual
            response_format={"type": "json_object"} # Force Groq to output valid JSON
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Analyze Agent Error: {e}")
        return {}