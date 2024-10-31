from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from get_docs import setup_model, search_docs


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, index, df, word_to_idx

    # Load the ML model
    model, index, df, word_to_idx = setup_model()
    yield
    # Clean up the ML models and release the resources
    model = None
    index = None
    df = None
    word_to_idx = None

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    # Allows all origins, or specify a list of allowed origins
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],   # Allows all HTTP methods
    allow_headers=["*"],   # Allows all headers
)


class QueryRequest(BaseModel):
    query: str


class DocumentResponse(BaseModel):
    rel_docs: List[str]
    rel_docs_sim: List[Union[float, int]]


@app.get("/")
async def read_root():
    return {"message": "Welcome to the search API. Use POST /search to send queries."}


@app.post("/search", response_model=DocumentResponse)
async def search(query_request: QueryRequest):

    # Ensure the model and resources are available
    if model is None or index is None or df is None or word_to_idx is None:
        return {"error": "Model or resources not initialized."}

    query = query_request.query
    # query_embedding = preprocess(query)
    rel_docs, distances = search_docs(query,  model, index, df, word_to_idx)
    return {
        "rel_docs": rel_docs,
        "rel_docs_sim": distances[0]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
