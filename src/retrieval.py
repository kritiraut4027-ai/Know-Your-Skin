from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple, Optional
import re
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class BaseRetriever(ABC):
    """Abstract Retriever interface (§8.1 of build spec)."""
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        """Returns list of (document_dict, score) tuples."""
        pass


class TfidfIngredientRetriever(BaseRetriever):
    """
    Default lightweight TF-IDF retriever (§8.1).
    Instant startup, <30 MB RAM footprint, zero external API cost.
    """
    def __init__(self, kb_path: Path, threshold: float = 0.35):
        self.kb_path = Path(kb_path)
        self.threshold = threshold
        self.documents: List[str] = []
        self.doc_mapping: List[Dict[str, Any]] = []
        self.kb: List[Dict[str, Any]] = []
        self._build_index()

    def _build_index(self):
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base not found: {self.kb_path}")
        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.kb = json.load(f)

        self.documents = []
        self.doc_mapping = []
        for entry in self.kb:
            text = (
                f"{entry.get('ingredient_name', '')} "
                f"{' '.join(entry.get('aliases', []))} "
                f"{entry.get('function', '')} "
                f"{' '.join(entry.get('common_concerns', []))} "
                f"{entry.get('caution_notes', '')}"
            )
            self.documents.append(text)
            self.doc_mapping.append(entry)

        # Domain-aware stopwords
        generic_terms = [
            'skin', 'face', 'cleanser', 'cleansers', 'product', 'products', 'used',
            'topical', 'does', 'work', 'role', 'mechanism', 'washes', 'formulation',
            'oil', 'extract', 'water', 'acid', 'treat', 'cure'
        ]
        base_stopwords = list(TfidfVectorizer(stop_words='english').get_stop_words())
        all_stopwords = list(set(base_stopwords + generic_terms))
        
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=all_stopwords)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        query_lower = query.lower()

        # 1. Exact name / alias boost
        exact_matches = []
        for entry in self.kb:
            name_pattern = r"\b" + re.escape(entry["ingredient_name"].lower()) + r"\b"
            if re.search(name_pattern, query_lower):
                exact_matches.append((entry, 1.0))
                continue
            for a in entry.get("aliases", []):
                alias_pattern = r"\b" + re.escape(a.lower()) + r"\b"
                if re.search(alias_pattern, query_lower):
                    exact_matches.append((entry, 0.95))
                    break

        if exact_matches:
            return exact_matches[:top_k]

        # 2. Vector cosine similarity
        query_vec = self.vectorizer.transform([query])
        if query_vec.nnz == 0:
            return []

        sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        best_indices = np.argsort(sims)[::-1]

        results = []
        for idx in best_indices[:top_k]:
            score = float(sims[idx])
            if score >= self.threshold:
                results.append((self.doc_mapping[idx], round(score, 3)))

        return results


_RETRIEVER_INSTANCE: Optional[TfidfIngredientRetriever] = None

def get_ingredient_retriever() -> TfidfIngredientRetriever:
    global _RETRIEVER_INSTANCE
    if _RETRIEVER_INSTANCE is None:
        kb_path = Path(__file__).resolve().parent.parent / "data" / "ingredient_kb.json"
        _RETRIEVER_INSTANCE = TfidfIngredientRetriever(kb_path=kb_path, threshold=0.35)
    return _RETRIEVER_INSTANCE
