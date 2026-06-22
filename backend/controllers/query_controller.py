import concurrent.futures
from flask import jsonify

# ---------------------------------------------------------
# Future Agent Imports (We will build these next)
# ---------------------------------------------------------
from rag.retriever import retrieve_relevant_context
from agents.coverage_agent import run_coverage_agent
from agents.exclusion_agent import run_exclusion_agent
from agents.waiting_period_agent import run_waiting_period_agent
# from agents.eligibility_agent import run_eligibility_agent
from agents.verdict_agent import run_verdict_agent
# from agents.auditor_agent import run_auditor_agent


def process_query(user_query: str):
    """
    Controller Logic: Orchestrates the multi-agent LLM pipeline.
    """
    print(f"User asked: '{user_query}'")
    
    try:

        # Retrieve context using the expanded parent-child logic
        print("1. Fetching relevant policy context from ChromaDB...")
        context = retrieve_relevant_context(user_query)
        # ---------------------------------------------------------
        # The Multi-Agent Orchestration Pipeline
        # ---------------------------------------------------------
        
        # Step 1: Specialist Agents Analyze the Query in Parallel (Conceptually)
        # print("2. Running Coverage Agent analysis...")
        # coverage_report = run_coverage_agent(user_query, context)
        # print("3. Running Exclusion Agent analysis...")
        # exclusion_report = run_exclusion_agent(user_query, context)
        # print("4. Running Waiting Period Agent analysis...")
        # waiting_period_report = run_waiting_period_agent(user_query, context)

        print("2. Running Specialist Agents concurrently...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks to the thread pool
            future_coverage = executor.submit(run_coverage_agent, user_query, context)
            future_exclusion = executor.submit(run_exclusion_agent, user_query, context)
            future_waiting = executor.submit(run_waiting_period_agent, user_query, context)
            
            # Gathering results as they complete
            coverage_report = future_coverage.result()
            exclusion_report = future_exclusion.result()
            waiting_period_report = future_waiting.result()

        print("5. Generating Final Verdict...")
        verdict_report = run_verdict_agent(coverage_report, exclusion_report, waiting_period_report)



        
        # eligibility_report = run_eligibility_agent(user_query)
        
        # Step 2: The Verdict Agent Synthesizes the Reports
        # print("2. Generating Verdict...")
        # verdict_report = run_verdict_agent(
        #     coverage_report, 
        #     exclusion_report, 
        #     waiting_period_report, 
        #     eligibility_report
        # )
        
        # Step 3: The Auditor Agent Verifies the Verdict
        # print("3. Auditing final decision...")
        # audit_result = run_auditor_agent(
        #     coverage_report,
        #     exclusion_report,
        #     waiting_period_report,
        #     eligibility_report,
        #     "N/A", # Payout agent placeholder if you didn't build one
        #     verdict_report
        # )
        
        # Step 4: Construct the final response payload
        # return jsonify({
        #     'status': 'success',
        #     'query': user_query,
        #     'verdict': verdict_report,
        #     'audit_status': audit_result.get('audit_status', 'UNKNOWN'),
        #     'confidence': audit_result.get('confidence', 'UNKNOWN'),
        #     'audit_reason': audit_result.get('audit_reason', '')
        # }), 200

        # --- TEMPORARY MOCK RESPONSE UNTIL AGENTS ARE BUILT ---
        return jsonify({
            'status': 'success',
            'query': user_query,
            'final_verdict': verdict_report,
            'reports': {
                'coverage': coverage_report,
                'exclusions': exclusion_report,
                'waiting_periods': waiting_period_report
            }
        }), 200

    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({
            'status': 'error',
            'message': f"Failed to process query: {str(e)}"
        }), 500