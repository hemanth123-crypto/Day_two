from __future__ import annotations
import logging
from typing import List, Optional
import numpy as np

from backend.app.config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)

_model_instance = None
_model_failed = False


def get_embedding_model():
    """
    Singleton loader for SentenceTransformer.
    Ensures model weights are loaded into memory exactly once across API calls.
    """
    global _model_instance, _model_failed
    if _model_instance is not None:
        return _model_instance
    if _model_failed:
        return None

    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading SentenceTransformer model: {EMBEDDING_MODEL}")
        _model_instance = SentenceTransformer(EMBEDDING_MODEL)
        return _model_instance
    except Exception as exc:
        logger.warning(f"Could not load SentenceTransformer ({exc}). Semantic search will fall back to TF-IDF.")
        _model_failed = True
        return None


def encode_query(query: str) -> Optional[np.ndarray]:
    """
    Generate normalized 1D or 2D embedding vector for a natural language query string.
    Returns float32 numpy array of shape (1, 384) or None if model unavailable.
    """
    model = get_embedding_model()
    if model is None:
        return None
    try:
        embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        return embedding.astype('float32')
    except Exception as exc:
        logger.error(f"Error encoding query: {exc}")
        return None


def encode_texts(texts: List[str]) -> Optional[np.ndarray]:
    """
    Batch encode a list of texts into normalized float32 embeddings.
    """
    model = get_embedding_model()
    if model is None:
        return None
    try:
        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
        return embeddings.astype('float32')
    except Exception as exc:
        logger.error(f"Error batch encoding texts: {exc}")
        return None
