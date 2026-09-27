from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.config import BASE_DIR, EMBEDDING_MODEL

SOURCE = BASE_DIR / 'data' / 'processed' / 'courses_cleaned.csv'
OUTPUT = BASE_DIR / 'vector_store' / 'course_embeddings.npy'
METADATA = BASE_DIR / 'vector_store' / 'course_ids.json'


def main():
    df = pd.read_csv(SOURCE)
    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = []
    for _, row in df.iterrows():
        text = ' '.join([
            str(row.get('course_name', '')),
            str(row.get('description', '')),
            str(row.get('skills', '')),
            str(row.get('difficulty', '')),
        ])
        texts.append(text)
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    np.save(OUTPUT, embeddings)
    pd.Series(df['course_id'].tolist()).to_json(METADATA, orient='records')
    print(f'Generated {len(embeddings)} embeddings and saved to {OUTPUT}')


if __name__ == '__main__':
    main()
