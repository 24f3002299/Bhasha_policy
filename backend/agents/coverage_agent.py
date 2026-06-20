import os
from groq import Groq

# Initialize the Groq client
# (Make sure your GROQ_API_KEY is still set in your terminal)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_coverage_agent(user_query: str, context: str) -> str:
    """
    Analyzes the retrieved policy context to determine if a specific treatment/event is covered.
    """
    print("Running Coverage Agent...")
    
    prompt = f"""You are an insurance coverage analyst.

Your job is to determine whether the user's query is covered by the insurance policy.
Use ONLY the provided context.
Your task is to determine whether the user's requested treatment is covered.

CRITICAL INSTRUCTIONS FOR DEDUCTIVE REASONING:
Insurance policies rarely list every specific surgery (e.g., "knee replacement"). Instead, they cover broad categories like "Inpatient Treatment", "Surgery", or "Surgical Procedures". 
1. If the policy covers "Surgery" or "Inpatient Care" generally, and the user is asking about a standard medical surgery, you MUST categorize it as IMPLICITLY COVERED.
2. Do not get distracted by exclusions for medical equipment (like "Knee Braces") when the user is asking about a surgery.
3. Use the expanded concepts to make logical links (e.g., Knee Replacement -> Joint Replacement -> Surgery).

Coverage may be stated:
- directly
- indirectly
- through broader categories
- through parent medical procedures

If the requested treatment belongs to a broader covered category, explain the relationship and determine whether coverage likely applies.

Do not require exact keyword matches.
If evidence is missing, say so.

Context:
{context}

Question:
{user_query}

Return your answer exactly in this format:
Coverage Status: [Covered / Not Covered / Indirectly Covered]
Reason: [Your reasoning]
Evidence: [Quote the relevant context]
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1, # Low temperature for factual consistency
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Coverage Agent Error: {e}")
        return "Coverage Status: ERROR\nReason: Agent failed to execute.\nEvidence: N/A"