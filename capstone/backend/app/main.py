from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import courses, recommendations, skills, learning_path, feedback
from backend.app.config import APP_NAME, DEBUG
from backend.app.database import Base, engine

from backend.app.utils.logging import RequestLoggingMiddleware, logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version='1.0.0', debug=DEBUG)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(courses.router, prefix='/api/v1')
app.include_router(recommendations.router, prefix='/api/v1')
app.include_router(skills.router, prefix='/api/v1')
app.include_router(learning_path.router, prefix='/api/v1')
app.include_router(feedback.router, prefix='/api/v1')


@app.get('/api/v1/health')
def health_check():
    return {'status': 'ok', 'app': APP_NAME}


@app.get('/')
def root():
    return {'message': APP_NAME}
