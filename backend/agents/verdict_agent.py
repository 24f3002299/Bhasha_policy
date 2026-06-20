import os
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_verdict_agent(coverage_report: str, exclusion_report: str, waiting_period_report: str) -> str:
    """
    Synthesizes the reports from the specialist agents to make a final Approved/Denied decision.
    """
    print("Running Verdict Agent (Chief Justice)...")
    
    prompt = f"""You are the Chief Claims Adjudicator.

Your job is to review the reports from three specialist agents and determine the final claim status.

Here are the reports:
---
COVERAGE REPORT:
{coverage_report}

EXCLUSION REPORT:
{exclusion_report}

WAITING PERIOD REPORT:
{waiting_period_report}
---

CRITICAL LOGIC RULES:
1. If the Exclusion Report says it is "Excluded", the final verdict MUST be "CLAIM DENIED".
2. If the Waiting Period Report says a waiting period applies, the final verdict MUST be "CLAIM DENIED".
3. If the Coverage Report says it is "Not Covered", the final verdict MUST be "CLAIM DENIED".
4. If Coverage is "Explicitly Covered" or "Implicitly Covered", AND no exclusions apply, AND no waiting periods apply, the final verdict is "CLAIM APPROVED".
5. If the reports conflict heavily, default to "MANUAL REVIEW REQUIRED".

Return your answer exactly in this format:
Final Verdict: [CLAIM APPROVED / CLAIM DENIED / MANUAL REVIEW REQUIRED]
Synthesis: [A clean, empathetic 2-3 sentence summary explaining the final decision based on the three reports.]
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