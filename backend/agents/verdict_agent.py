import os
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_verdict_agent(coverage_report: str, exclusion_report: str, waiting_period_report: str) -> str:
    """
    Synthesizes the reports from the specialist agents to make a final Approved/Denied decision.
    """
    print("Running Verdict Agent (Chief Justice)...")
    
    prompt = f"""You are an empathetic, objective, and helpful Insurance Policy Explainer.

Your job is to read the reports from three specialist agents and explain the coverage to the user in simple, plain language. 

CRITICAL RULES:
1. You DO NOT approve or deny claims. You are not a judge. 
2. Your purpose is to inform, alert, and educate the user based strictly on the policy text.
3. Keep the tone gentle and helpful. Never use harsh words like "DENIED" or "REJECTED" unnecessarily.
4. Translate complex jargon into simple concepts.

Here are the reports from your specialists:
---
COVERAGE REPORT:
{coverage_report}

EXCLUSION REPORT:
{exclusion_report}

WAITING PERIOD REPORT:
{waiting_period_report}
---

Synthesize the final answer using EXACTLY this format (do not use markdown formatting like asterisks, just the plain text labels):

Coverage Status: [Choose one: Covered / Covered after some time (Delayed) / Not Covered / Unclear]

Reason: [Explain simply and gently under what conditions this is covered or why it is excluded based on the reports.]

Definitions: [Briefly define any jargon you used in the reason, such as 'Waiting period', 'Pre-existing diseases', or 'Continuous coverage'. Keep definitions simple. If no jargon was used, write N/A.]

Evidence: [Combine the specific clauses and page numbers provided in the specialist reports.]
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0, # 0.0 because this is strict rules-based synthesis
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Verdict Agent Error: {e}")
        return "Final Verdict: ERROR\nSynthesis: Agent failed to execute."