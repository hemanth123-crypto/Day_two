from __future__ import annotations
import sys
from pathlib import Path

import faiss
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.config import BASE_DIR

SOURCE = BASE_DIR / 'data' / 'processed' / 'courses_cleaned.csv'
EMBEDDINGS = BASE_DIR / 'vector_store' / 'course_embeddings.npy'
INDEX_PATH = BASE_DIR / 'vector_store' / 'course_index.faiss'


def main():
    if not EMBEDDINGS.exists():
        raise FileNotFoundError('Embeddings not found. Run build_embeddings.py first.')
    df = pd.read_csv(SOURCE)
    embeddings = np.load(EMBEDDINGS).astype('float32')

    # Ensure vectors are L2-normalized for exact cosine similarity
    faiss.normalize_L2(embeddings)

    # IndexFlatIP directly calculates Inner Product (which equals Cosine Similarity for normalized vectors)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    print(f'Generated FAISS IndexFlatIP (Cosine Similarity) with {index.ntotal} courses saved to {INDEX_PATH}')


if __name__ == '__main__':
    main()
