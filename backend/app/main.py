from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="DocuMind API",
    description="Intelligent Document Processing API",
    version="1.0.0",
)
app.include_router(
    search_router,
    prefix="/api/search",
    tags=["Search"],
)
app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat"],
)
# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(
    documents_router,
    prefix="/api/documents",
    tags=["Documents"],
)


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to DocuMind API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }