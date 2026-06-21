import os
# from groq import Groq

# groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
from routes.llm_routes import call_ai_model

def run_waiting_period_agent(user_query: str, context: str) -> str:
    """
    Scans the retrieved policy context strictly for waiting periods applicable to the claim.
    """
    print("Running Waiting Period Agent...")
    
    prompt = f"""You are a precise Waiting Period Analyst.

Your ONLY responsibility is finding waiting periods.

You help users understand waiting periods within insurance policies.

Use ONLY the provided policy context.

Rules:

Identify any waiting periods relevant to the user's question.
Quote the exact waiting period duration.
Explain what the waiting period means in plain language.
If no waiting period is found, say so.
Do not make final claim decisions.

CRITICAL INSTRUCTIONS:
1. Ignore general coverage clauses and general exclusions.
2. Focus ONLY on time-based restrictions (e.g., "24 months", "30 days", "pre-existing diseases").
3. Check if the specific treatment or category in the user's query is subject to a waiting period.
4. If no waiting period is found for the specific request, explicitly state "NO_WAITING_PERIOD_FOUND".

Context:
{context}

Question:
{user_query}

Return EXACTLY in this format:

Waiting Period Assessment

Waiting Period Found:
[Duration / None Found / Unclear]

What We Found:
[Relevant waiting period details.]

Supporting Evidence:
[Quote relevant clauses.]

Plain Language Explanation:
[Explain the waiting period in simple language.]

Important Note:
Waiting periods are only one factor considered during claim review.
"""

    try:
        # response = groq_client.chat.completions.create(
        #     model="llama-3.3-70b-versatile",
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.0, # 0.0 because time limits are strict facts
        #     max_tokens=300
        # )
        # return response.choices[0].message.content.strip()
        return call_ai_model(prompt)
    except Exception as e:
        print(f"Waiting Period Agent Error: {e}")
        return "Waiting Period Status: ERROR\nReason: Agent failed to execute.\nEvidence: N/A"