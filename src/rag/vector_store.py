from sentence_transformers import SentenceTransformer
import faiss
import torch
class FAISSVectorStore:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model, device="cuda" if torch.cuda.is_available() else "cpu")
        self.dimension = 384  
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []

    def from_texts(self, texts, metadatas):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        self.index.add(embeddings)
        self.texts = texts
        self.metadata = metadatas
        return self

    def similarity_search(self, query, k=5):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx != -1:  
                results.append({"text": self.texts[idx], "metadata": self.metadata[idx], "distance": dist})
        return results