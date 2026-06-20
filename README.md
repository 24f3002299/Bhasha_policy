# Insurance Policy Intelligence Assistant

## Overview

Insurance policies are often lengthy and difficult to understand, containing complex clauses related to coverage, exclusions, waiting periods, co-payments, deductibles, and claim conditions. Policyholders frequently struggle to determine whether a treatment or procedure is covered until they attempt to file a claim.

Insurance Policy Intelligence Assistant is an Agentic RAG (Retrieval-Augmented Generation) system that helps users understand insurance policies through evidence-backed reasoning and transparent decision support.

Built for **The Arch: RAG and Agentic AI Hackathon**.

---

## Problem Statement

Traditional chatbots often provide generic answers and may miss important policy clauses. Insurance decisions typically depend on multiple interconnected sections spread across a document.

Users need a system that can:

* Understand policy documents
* Retrieve relevant clauses
* Analyze exclusions and waiting periods
* Provide evidence-backed answers
* Compare insurance policies
* Explain complex legal language in simple terms

---

## Solution

Our system allows users to upload insurance policy documents and ask real-world questions such as:

* Is knee replacement surgery covered?
* Does a waiting period apply?
* What exclusions affect this claim?
* How much reimbursement can I expect?
* Which policy is better for my situation?

Instead of simply generating answers, the system retrieves relevant policy clauses, reasons over them, and produces transparent, citation-backed responses.

---

## Key Features

### Policy Question Answering

Upload a policy document and ask natural language questions.

### Coverage Analysis

Determine whether a treatment, procedure, or service is covered under the policy.

### Exclusion Detection

Identify policy exclusions that may impact eligibility.

### Waiting Period Analysis

Analyze waiting period clauses and their applicability.

### Evidence-Based Responses

Provide answers supported by relevant policy sections.

### Policy Comparison

Compare multiple insurance policies across coverage, exclusions, limits, and waiting periods.

### Simplified Explanations

Translate complex insurance terminology into user-friendly language.

---

## System Architecture

User Question
↓
Document Retrieval
↓
Coverage Analysis Agent
↓
Exclusion Analysis Agent
↓
Waiting Period Analysis Agent
↓
Verdict Generation Agent
↓
Evidence Aggregation
↓
Final Response

---

## Tech Stack

### Backend

* Python
* Flask

### AI & RAG

* Gemini API
* LangChain
* ChromaDB
* Embeddings

### Document Processing

* PyMuPDF
* PDF Processing Pipeline

### Frontend

* HTML
* CSS
* JavaScript
* Vue.js (optional)

---

## Project Structure

```text
insurance-policy-intelligence-assistant/

├── agents/
│   ├── coverage_agent.py
│   ├── exclusion_agent.py
│   ├── waiting_period_agent.py
│   └── verdict_agent.py
│
├── rag/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   └── retriever.py
│
├── uploads/
│
├── templates/
│
├── static/
│
├── app.py
│
└── README.md
```

## Current Development Status

* [x] PDF Text Extraction
* [x] Document Chunking
* [x] Embedding Generation
* [x] Semantic Retrieval
* [x] Coverage Agent
* [x] Exclusion Agent
* [x] Waiting Period Agent
* [x] Verdict Agent
* [ ] Policy Comparison
* [ ] Frontend Integration

---

## Future Enhancements

* Multilingual Support
* Policy Comparison Dashboard
* Claim Eligibility Scoring
* Reimbursement Estimation
* Regional Language Explanations
* Advanced Agent Orchestration

---

## Team

Developed as part of The Arch: RAG and Agentic AI Hackathon.

Team Members:

* Azkiya
* Priya
* Siddhi

---

## Vision

Our goal is to make insurance policies understandable, transparent, and accessible through trustworthy AI-powered decision support.
