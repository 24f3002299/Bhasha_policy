import os
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_exclusion_agent(user_query: str, context: str) -> str:
    """
    Scans the retrieved policy context strictly for exclusions or reasons to deny the claim.
    """
    print("Running Exclusion Agent...")
    
    prompt = f"""You are a strict Insurance Exclusion Analyst.

Your ONLY job is to identify if the user's request is specifically excluded in the policy context.

CRITICAL INSTRUCTIONS:
1. Ignore general coverage clauses. You are only looking for EXCLUSIONS.
2. Ignore waiting periods and eligibility rules (another agent handles those).
3. If no exclusion is found, you MUST explicitly say "NO_EXCLUSION_FOUND".
4. Do not make assumptions. If it doesn't say it's excluded, then it is not excluded.

Context:
{context}

Question:
{user_query}

Return your answer exactly in this format:
Exclusion Status: [Excluded / NO_EXCLUSION_FOUND]
Reason: [Explain why it is excluded, or state that no exclusion text was found]
Evidence: [Quote the exact exclusion clause, or state N/A]
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0, # 0.0 because exclusions are black-and-white facts
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Exclusion Agent Error: {e}")
        return "Exclusion Status: ERROR\nReason: Agent failed to execute.\nEvidence: N/A"