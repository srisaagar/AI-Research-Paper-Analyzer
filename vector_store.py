import faiss
import numpy as np


class VectorStore:

    def __init__(self):
        self.index = None
        self.text_chunks = []

    def build_index(self, embeddings, chunks):

        dimension = len(embeddings[0])

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(np.array(embeddings))

        self.text_chunks = chunks

    def search(self, query_embedding, k=3):

        D, I = self.index.search(np.array(query_embedding), k)

        results = []

        for i in I[0]:
            results.append(self.text_chunks[i])

        return results