InsightPaper Pro – AI Research Paper Analyzer

InsightPaper Pro is an AI-powered research intelligence platform that allows users to upload academic papers and interact with them using advanced Large Language Models and Retrieval-Augmented Generation (RAG). The system analyzes research papers to extract insights, generate summaries, detect research gaps, visualize citation networks, and even automatically generate presentation slides.

The platform is designed to assist researchers, students, and academics in understanding complex research papers quickly and efficiently.

Features
AI Research Paper Analysis

Automatically analyzes uploaded research papers and extracts meaningful insights.

Research Paper Summarization

Generates a concise summary including the problem, proposed solution, results, and conclusion.

Key Contribution Extraction

Identifies the main contributions of a research paper.

Methodology Detection

Extracts algorithms, techniques, and methods used in the research.

Chat with Research Papers (RAG)

Ask questions about uploaded papers and receive answers grounded in the document context.

Citation Graph Visualization

Builds a citation network showing relationships between referenced papers.

Similar Research Finder

Uses semantic embeddings to find related research passages and topics.

Research Gap Detection

Identifies limitations in current work and suggests potential future research directions.

Automatic PPT Generator

Converts research papers into structured presentation slides automatically using AI.

System Architecture
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
Semantic Retrieval
   │
   ▼
LLM Reasoning
(Ollama + Llama3)
   │
   ▼
Streamlit UI
Technologies Used

Python
Streamlit
Ollama
Llama 3
Sentence Transformers
FAISS Vector Search
NetworkX
Plotly
python-pptx

Project Structure
research-paper-analyzer
│
├── app.py
├── analyzer.py
├── embedder.py
├── pdf_processor.py
├── vector_store.py
├── citation_graph.py
├── ppt_generator.py
├── requirements.txt
└── README.md
Installation
1 Install dependencies
pip install -r requirements.txt
2 Install Ollama

Download and install Ollama from

https://ollama.com

Then download the LLM model:

ollama pull llama3
Run the Application
streamlit run app.py

Then open the application in your browser:

http://localhost:8501
