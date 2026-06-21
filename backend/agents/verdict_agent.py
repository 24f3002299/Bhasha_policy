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

Return EXACTLY in this format:
ormat your output EXACTLY like this (use these exact text headers, do not use markdown asterisks):

Coverage Status: [Write a highly accurate, short status label (1 to 6 words). Examples: "Fully Covered", "Not Covered", "Covered up to Sub-Limit", "Covered after 24 Months", "Covered on Co-Pay basis". You are free to create the most accurate short phrase based on the reports.]

Reason: [Explain exactly why it has this status in simple terms based on the reports.]

Definitions: [Briefly define any insurance jargon used in your Reason, such as 'Waiting Period' or 'Pre-existing Disease'. If no jargon is used, write "N/A" and it will be hidden.]

Exception: [Identify any explicit exceptions to the rules found in the reports. If none, write "None mentioned in the policy."]

Expenses Covered: [CRITICAL INSTRUCTION: ONLY include this if the user is asking about a specific medical treatment, surgery, or hospital admission. If they are, list the specific types of expenses paid out. If it is a general question, do not include this header at all.]

Evidence: 
[List each piece of evidence on a NEW LINE using a bullet point. Format exactly like this:
• Page X, Clause Y: "Exact quote..."
• Page Z, Clause W: "Exact quote..."]


Important Note:
This summary is intended to help users understand policy terms and conditions. Final claim decisions depend on the insurer's review and supporting claim documentation.


"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0, # 0.0 because this is strict rules-based synthesis
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Verdict Agent Error: {e}")
        return "Final Verdict: ERROR\nSynthesis: Agent failed to execute."