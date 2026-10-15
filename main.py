from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import notes, graph

app = FastAPI(
    title="Personal Knowledge Graph API",
    description=(
        "Create notes, connect knowledge, manage tags, "
        "and explore backlinks."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router)
app.include_router(graph.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Personal Knowledge Graph API is running"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}