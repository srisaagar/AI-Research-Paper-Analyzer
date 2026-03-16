import ollama
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
model_embed = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------
# LLM CALL
# -------------------------------
def ask_llm(prompt):

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Error generating response: {e}"


# -------------------------------
# PAPER SUMMARY
# -------------------------------
def summarize_paper(text):

    prompt = f"""
You are a research assistant.

Summarize the following research paper clearly.

Include:
• Problem
• Proposed solution
• Key results
• Conclusion

Paper:
{text[:4000]}
"""

    return ask_llm(prompt)


# -------------------------------
# CONTRIBUTION EXTRACTION
# -------------------------------
def extract_contributions(text):

    prompt = f"""
Extract the key contributions of this research paper.

Return the contributions as bullet points.

Paper:
{text[:4000]}
"""

    return ask_llm(prompt)


# -------------------------------
# METHODOLOGY EXTRACTION
# -------------------------------
def extract_methodology(text):

    prompt = f"""
Identify the methodology, algorithms, models, or techniques used in this research paper.

Paper:
{text[:4000]}
"""

    return ask_llm(prompt)


# -------------------------------
# RAG QUESTION ANSWERING
# -------------------------------
def ask_question(question, vector_store, chunks):

    query_embedding = model_embed.encode([question])

    query_embedding = np.array(query_embedding)

    results = vector_store.search(query_embedding, k=3)

    context = "\n".join(results)

    prompt = f"""
You are an AI research assistant.

Use the following research paper context to answer the question.

Context:
{context}

Question:
{question}

Answer clearly using the information from the context.
"""

    return ask_llm(prompt)


# -------------------------------
# SIMILAR PAPER FINDER
# -------------------------------
def find_similar_papers(query, vector_store):

    query_embedding = model_embed.encode([query])

    query_embedding = np.array(query_embedding)

    results = vector_store.search(query_embedding, k=5)

    return results


# -------------------------------
# RESEARCH GAP DETECTOR
# -------------------------------
def detect_research_gaps(vector_store):

    search_query = "limitations future work challenges open problems research gaps"

    query_embedding = model_embed.encode([search_query])

    query_embedding = np.array(query_embedding)

    results = vector_store.search(query_embedding, k=6)

    context = "\n".join(results)

    prompt = f"""
You are an expert research analyst.

Analyze the following research paper excerpts and identify:

1. Existing research areas
2. Limitations of current approaches
3. Research gaps that remain unexplored
4. Possible future research directions

Research Paper Context:
{context}

Provide a structured analysis.
"""

    return ask_llm(prompt)