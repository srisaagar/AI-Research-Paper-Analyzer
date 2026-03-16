**📄 InsightPaper Pro – AI Research Paper Analyzer**

InsightPaper Pro is an** **AI-powered research paper analysis**** platform that allows users to upload academic PDFs and interact with them using **Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).**

The system automatically analyzes research papers to extract insights such as** **summaries, key contributions, methodologies, citation networks, research gaps, and presentation slides.**
**
It runs completely locally using Ollama + Llama3, enabling secure and private research analysis.

**🚀 Features**
**📑 Research Paper Summarization**

Automatically generates a concise summary of uploaded research papers.

**⭐ Key Contribution Extraction**

Identifies the main innovations and contributions of the paper.

**⚙ Methodology Detection**

Extracts the algorithms, techniques, and methods used in the research.

**🕸 Citation Graph Visualization**

Builds a citation network showing relationships between referenced works.

**💬 Chat with Research Papers (RAG)**

Ask natural language questions about the uploaded papers.

**Example questions:**
**
What problem does this paper solve?

What dataset is used?

What algorithm is proposed?
**
**🔬 Research Gap Detection**

Identifies potential research gaps and future research opportunities.

**🔍 Similar Research Finder**

Uses semantic embeddings to find related research passages.

**📊 Automatic PPT Generator**

Converts research papers into conference-style PowerPoint presentations..

**🧠 System Architecture**

**PDF Upload
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
AI Insights + Visualization
(Streamlit UI)**

**🛠 Tech Stack**

**| Component      | Technology            |
| -------------- | --------------------- |
| Frontend       | Streamlit             |
| LLM            | Ollama (Llama3)       |
| Embeddings     | Sentence Transformers |
| Vector Search  | FAISS                 |
| Visualization  | Plotly + NetworkX     |
| PDF Processing | PyPDF                 |
| PPT Generation | python-pptx           |
| Language       | Python                |
**

**▶ Run the Application
streamlit run app.py

Open in browser:

http://localhost:8501**
