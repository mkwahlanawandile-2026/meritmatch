"""Semantic similarity matching for MeritMatch."""

from typing import Dict, Optional

from config import EMBEDDING_MODEL, SEMANTIC_MATCH_THRESHOLD


_model = None


def load_embedding_model():
    """Load the configured sentence-transformer model lazily."""
    global _model

    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(EMBEDDING_MODEL)

    return _model


def calculate_semantic_similarity(
    candidate_text: str,
    job_text: str,
) -> float:
    """Calculate semantic similarity between candidate and job text."""

    if not candidate_text or not job_text:
        return 0.0

    model = load_embedding_model()

    embeddings = model.encode(
        [candidate_text, job_text],
        normalize_embeddings=True,
    )

    similarity = float(embeddings[0] @ embeddings[1])

    return round(
        max(0.0, min(similarity, 1.0)) * 100,
        2,
    )


def match_semantic_requirements(
    candidate_text: str,
    job_text: str,
) -> Dict:
    """Return semantic similarity and threshold information."""

    score = calculate_semantic_similarity(
        candidate_text,
        job_text,
    )

    threshold_score = SEMANTIC_MATCH_THRESHOLD * 100

    return {
        "score": score,
        "threshold": threshold_score,
        "meets_threshold": score >= threshold_score,
        "model": EMBEDDING_MODEL,
    }
