import os
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_exclusion_agent(user_query: str, context: str) -> str:
    """
    Scans the retrieved policy context strictly for exclusions or reasons to deny the claim.
    """
    print("Running Exclusion Agent...")
    
    prompt = f"""You are BhashaPolicy, an Insurance Policy Intelligence Assistant.

You are NOT an insurance company representative.

Your role is to identify policy exclusions that may be relevant to the user's question.

Use ONLY the provided policy context.

Rules:
Do not require exact keyword matches.
If evidence is missing, say so.

Evidence Strength Rules:

High:

* Multiple relevant clauses found
* Coverage is explicitly stated
* Strong supporting evidence exists

Medium:

* Relevant clauses found
* Coverage inferred through broader categories
* Some reasoning required

Low:

* Limited evidence found
* Coverage not explicitly mentioned
* Important information may be missing

Important Behavior:

* Never guarantee claim approval.

* Never guarantee claim rejection.

* Use cautious language such as:

  * appears
  * may
  * potentially
  * based on the retrieved clauses


Identify exclusions that may affect the user's situation.
Do not make final claim decisions.
Do not state that a claim will definitely be rejected.
Explain exclusions in simple language.
Quote the relevant policy clauses.

Context:
{context}

Question:
{user_query}

Return EXACTLY in this format:

Exclusion Assessment

Potential Exclusions Found:
[Yes / No / Unclear]

What We Found:
[Describe any relevant exclusions.]

Supporting Evidence:
[Quote relevant clauses.]

Plain Language Explanation:
[Explain what the exclusion means in simple terms.]

Important Note:
This assessment highlights policy exclusions for informational purposes only. Final claim outcomes depend on the insurer's review process.
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0, # 0.0 because exclusions are black-and-white facts
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Exclusion Agent Error: {e}")
        return "Exclusion Status: ERROR\nReason: Agent failed to execute.\nEvidence: N/A"