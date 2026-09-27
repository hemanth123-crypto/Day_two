from __future__ import annotations
import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.app.config import BASE_DIR, TOP_K
from backend.app.services.embedding_service import encode_query

logger = logging.getLogger(__name__)

COURSES_PATH = BASE_DIR / 'data' / 'processed' / 'courses_cleaned.csv'
INDEX_PATH = BASE_DIR / 'vector_store' / 'course_index.faiss'
EMBEDDINGS_PATH = BASE_DIR / 'vector_store' / 'course_embeddings.npy'

# Singleton caches
_cached_df: Optional[pd.DataFrame] = None
_cached_faiss_index = None
_faiss_load_failed = False
_cached_tfidf_vectorizer = None
_cached_tfidf_matrix = None


def _json_safe(value: Any) -> Any:
    """Ensure floats with NaN/Inf and numpy types serialize cleanly to JSON."""
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, 4)
    if isinstance(value, (np.floating, np.float32, np.float64)):
        v = float(value)
        return None if (math.isnan(v) or math.isinf(v)) else round(v, 4)
    if isinstance(value, (np.integer, np.int64, np.int32)):
        return int(value)
    return value


def _load_processed_courses() -> pd.DataFrame:
    """Load and cache processed courses dataframe."""
    global _cached_df
    if _cached_df is not None:
        return _cached_df
    if not COURSES_PATH.exists():
        raise FileNotFoundError(f'Processed course dataset is missing at {COURSES_PATH}. Run preprocessing first.')
    df = pd.read_csv(COURSES_PATH)
    # Fill NAs
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['course_name'] = df['course_name'].fillna('Unknown Course')
    df['description'] = df['description'].fillna('')
    df['skills'] = df['skills'].fillna('')
    df['difficulty'] = df['difficulty'].fillna('Unknown')
    df['organization'] = df['organization'].fillna('Unknown')
    df['url'] = df['url'].fillna('')
    df['search_text'] = df['search_text'].fillna('')
    _cached_df = df
    return _cached_df


def _get_faiss_index():
    """Load and cache FAISS index singleton."""
    global _cached_faiss_index, _faiss_load_failed
    if _cached_faiss_index is not None:
        return _cached_faiss_index
    if _faiss_load_failed:
        return None
    if not INDEX_PATH.exists():
        logger.warning(f"FAISS index not found at {INDEX_PATH}.")
        _faiss_load_failed = True
        return None
    try:
        import faiss
        index = faiss.read_index(str(INDEX_PATH))
        _cached_faiss_index = index
        logger.info(f"Loaded FAISS index with {index.ntotal} vectors.")
        return _cached_faiss_index
    except Exception as exc:
        logger.warning(f"Failed to load FAISS index ({exc}). Falling back to TF-IDF search.")
        _faiss_load_failed = True
        return None


def _get_tfidf_model(df: pd.DataFrame):
    """Singleton cache for TF-IDF fallback vectorizer."""
    global _cached_tfidf_vectorizer, _cached_tfidf_matrix
    if _cached_tfidf_vectorizer is not None and _cached_tfidf_matrix is not None:
        return _cached_tfidf_vectorizer, _cached_tfidf_matrix
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000, ngram_range=(1, 2))
    corpus = df['search_text'].fillna('').tolist()
    matrix = vectorizer.fit_transform(corpus)
    _cached_tfidf_vectorizer = vectorizer
    _cached_tfidf_matrix = matrix
    return _cached_tfidf_vectorizer, _cached_tfidf_matrix


def _fallback_tfidf_search(query: str, top_k: int = TOP_K, df: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    """TF-IDF keyword / n-gram similarity fallback search."""
    if df is None:
        df = _load_processed_courses()
    if df.empty:
        return []

    vectorizer, matrix = _get_tfidf_model(df)
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, matrix).ravel()

    # Domain keyword boosting for specific terms
    query_lower = str(query).lower()
    boost_keywords = ['cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'linux', 'devops', 'machine learning', 'python', 'sql']
    boosted = np.copy(sims)

    for idx, row in df.iterrows():
        combined = f"{row.get('course_name', '')} {row.get('skills', '')} {row.get('description', '')}".lower()
        for kw in boost_keywords:
            if kw in query_lower and kw in combined:
                boosted[idx] += 0.25

    top_indices = np.argsort(boosted)[::-1][:top_k]
    results = []
    for idx in top_indices:
        row = df.iloc[idx]
        res = {
            'course_id': str(row.get('course_id', f'course_{idx:04d}')),
            'course_name': str(row.get('course_name', '')),
            'description': str(row.get('description', '')),
            'difficulty': str(row.get('difficulty', 'Unknown')),
            'rating': float(row['rating']) if pd.notna(row.get('rating')) else 0.0,
            'organization': str(row.get('organization', '')),
            'url': str(row.get('url', '')),
            'skills': str(row.get('skills', '')),
            'search_text': str(row.get('search_text', '')),
            'semantic_score': float(max(0.0, min(1.0, boosted[idx]))),
            'retrieval_method': 'tfidf_fallback',
        }
        results.append(_json_safe(res))
    return results


def search_courses(
    query: str,
    top_k: int = TOP_K,
    difficulty: Optional[str] = None,
    min_rating: Optional[float] = None,
    organization: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search courses using FAISS dense vector similarity, with fallback to TF-IDF.
    Supports optional filters for difficulty, min_rating, and organization.
    """
    if not query or not str(query).strip():
        raise ValueError('Query cannot be empty.')

    df = _load_processed_courses()
    if df.empty:
        return []

    # Attempt FAISS semantic search
    faiss_index = _get_faiss_index()
    q_emb = encode_query(query) if faiss_index is not None else None

    # Overfetch candidates to allow post-filtering and reranking
    fetch_k = min(len(df), max(top_k * 4, 30))

    if faiss_index is not None and q_emb is not None:
        try:
            # FAISS IndexFlatIP returns inner product (cosine similarity)
            similarities, indices = faiss_index.search(q_emb, fetch_k)
            sims = similarities[0]
            idxs = indices[0]

            candidates = []
            for sim, idx in zip(sims, idxs):
                if idx < 0 or idx >= len(df):
                    continue
                row = df.iloc[idx]

                # Normalized semantic similarity mapped to [0, 1]
                # Cosine similarity is [-1, 1], typically [0.2, 0.95] for relevant items
                norm_sim = float(max(0.0, min(1.0, (sim + 1.0) / 2.0 if sim < 0 else sim)))

                res = {
                    'course_id': str(row.get('course_id', f'course_{idx:04d}')),
                    'course_name': str(row.get('course_name', '')),
                    'description': str(row.get('description', '')),
                    'difficulty': str(row.get('difficulty', 'Unknown')),
                    'rating': float(row['rating']) if pd.notna(row.get('rating')) else 0.0,
                    'organization': str(row.get('organization', '')),
                    'url': str(row.get('url', '')),
                    'skills': str(row.get('skills', '')),
                    'search_text': str(row.get('search_text', '')),
                    'semantic_score': norm_sim,
                    'retrieval_method': 'faiss_dense',
                }
                candidates.append(res)

            # Apply filters if provided
            filtered = _apply_filters(candidates, difficulty, min_rating, organization)
            return [_json_safe(c) for c in filtered[:top_k]]
        except Exception as exc:
            logger.warning(f"FAISS search failed ({exc}). Falling back to TF-IDF.")

    # Fallback to TF-IDF
    fallback_results = _fallback_tfidf_search(query, top_k=fetch_k, df=df)
    filtered = _apply_filters(fallback_results, difficulty, min_rating, organization)
    return [_json_safe(c) for c in filtered[:top_k]]


def _apply_filters(
    courses: List[Dict[str, Any]],
    difficulty: Optional[str] = None,
    min_rating: Optional[float] = None,
    organization: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter course candidates by difficulty, rating, and organization."""
    filtered = courses
    if difficulty and difficulty.lower() not in {'all', 'any', ''}:
        filtered = [c for c in filtered if str(c.get('difficulty', '')).lower() == difficulty.lower()]
    if min_rating is not None and min_rating > 0:
        filtered = [c for c in filtered if float(c.get('rating') or 0.0) >= min_rating]
    if organization and organization.lower() not in {'all', 'any', ''}:
        filtered = [c for c in filtered if organization.lower() in str(c.get('organization', '')).lower()]
    return filtered
