# InsightPaper Pro – AI Research Paper Analyzer

InsightPaper Pro is an AI-powered research paper analysis tool that allows users to upload academic PDFs and interact with them using natural language.

The system uses **Retrieval-Augmented Generation (RAG)** with a local LLM to summarize papers, extract insights, answer questions, and detect research gaps.

---

## Features

- Upload multiple research papers (PDF)
- AI-based research paper summarization
- Extract key contributions
- Identify methodology used in papers
- Chat with research papers using RAG
- Similar research finder using semantic search
- Citation graph visualization
- Research gap detection across papers

---

## Tech Stack

- Python
- Streamlit
- Ollama (Llama3)
- Sentence Transformers
- FAISS Vector Search
- NetworkX
- Plotly

---

## System Architecture
PDF Upload
│
▼
Text Extraction
│
▼
Text Chunking
│
▼
Embedding Generation
(Sentence Transformers)
│
▼
Vector Database
(FAISS)
│
▼
Retrieval (Semantic Search)
│
▼
LLM Reasoning
(Ollama + Llama3)
│
▼
AI Response (Streamlit UI)

---

## Installation

### 1 Install dependencies

```bash
pip install -r requirements.txt





streamlit run app.py
