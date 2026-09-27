from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = BASE_DIR / 'backend'
DATA_DIR = BASE_DIR / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'
VECTOR_STORE_DIR = BASE_DIR / 'vector_store'
RAW_DATA_DIR = DATA_DIR / 'raw'

APP_NAME = os.getenv('APP_NAME', 'University Course Finder')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
TOP_K = int(os.getenv('TOP_K', '10'))
SEMANTIC_WEIGHT = float(os.getenv('SEMANTIC_WEIGHT', '0.60'))
SKILL_WEIGHT = float(os.getenv('SKILL_WEIGHT', '0.20'))
DIFFICULTY_WEIGHT = float(os.getenv('DIFFICULTY_WEIGHT', '0.10'))
RATING_WEIGHT = float(os.getenv('RATING_WEIGHT', '0.10'))
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./course_finder.db')
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openrouter')
LLM_API_KEY = os.getenv('LLM_API_KEY', '')

# OpenRouter LLM Configuration for RAG answer generation
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.5-flash')
OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')


def ensure_directories() -> None:
    for directory in [RAW_DATA_DIR, PROCESSED_DIR, VECTOR_STORE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


ensure_directories()
