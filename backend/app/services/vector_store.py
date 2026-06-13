from functools import lru_cache

from app.core.config import settings


class CandidateVectorStore:
    def __init__(self) -> None:
        import chromadb
        from sentence_transformers import SentenceTransformer

        self.client = chromadb.PersistentClient(path=settings.chroma_path)
        self.collection = self.client.get_or_create_collection("candidates")
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def upsert_candidate(self, candidate_id: int, text: str, metadata: dict) -> None:
        embedding = self.encoder.encode(text).tolist()
        self.collection.upsert(
            ids=[str(candidate_id)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
        )

    def search(self, query: str, limit: int = 10) -> list[dict]:
        embedding = self.encoder.encode(query).tolist()
        results = self.collection.query(query_embeddings=[embedding], n_results=limit)
        return [
            {
                "candidate_id": int(results["ids"][0][idx]),
                "document": results["documents"][0][idx],
                "metadata": results["metadatas"][0][idx],
                "distance": results["distances"][0][idx],
            }
            for idx in range(len(results["ids"][0]))
        ]

@lru_cache
def get_vector_store() -> CandidateVectorStore:
    return CandidateVectorStore()


class LightweightVectorStore:
    def __init__(self) -> None:
        self.documents: dict[int, tuple[str, dict]] = {}

    def upsert_candidate(self, candidate_id: int, text: str, metadata: dict) -> None:
        self.documents[candidate_id] = (text, metadata)

    def search(self, query: str, limit: int = 10) -> list[dict]:
        terms = {term.lower() for term in query.split() if len(term) > 2}
        scored = []
        for candidate_id, (document, metadata) in self.documents.items():
            haystack = f"{document} {metadata}".lower()
            score = sum(1 for term in terms if term in haystack)
            if score:
                scored.append({
                    "candidate_id": candidate_id,
                    "document": document[:1000],
                    "metadata": metadata,
                    "distance": 1 / score,
                })
        return sorted(scored, key=lambda row: row["distance"])[:limit]


@lru_cache
def get_lightweight_vector_store() -> LightweightVectorStore:
    return LightweightVectorStore()
