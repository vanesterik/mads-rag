from typing import Dict

from chromadb import PersistentClient
from fastapi import FastAPI
from pydantic import BaseModel

from rag.common.config import COLLECTION_DIR, COLLECTION_NAME
from rag.core.generating import generate_response
from rag.core.retrieving import retrieve_documents


class InputData(BaseModel):
    prompt: str


class OutputData(BaseModel):
    response: str


app = FastAPI()
db_client = PersistentClient(path=COLLECTION_DIR)
db_collection = db_client.get_collection(name=COLLECTION_NAME)


@app.post("/generate")
def generate(input: InputData) -> OutputData:

    documents = retrieve_documents(collection=db_collection, query=input.prompt)
    response = generate_response(
        prompt=input.prompt,
        documents=documents,
    )
    return OutputData(response=response)


@app.get("/")
def read_root() -> Dict[str, str]:
    return {
        "app": "MADS-RAG",
        "version": "0.1.0",
    }
