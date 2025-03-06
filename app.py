from os import getenv
from typing import Annotated, Dict, List

import chromadb
import jwt
import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from openai import OpenAI
from pydantic import BaseModel

from rag.common.config import COLLECTION_DIR, COLLECTION_NAME, ENCRYPTION_ALGORITHM
from rag.core.generating import generate_answer
from rag.core.retrieving import retrieve_documents

# Define secret key
load_dotenv(find_dotenv())
SECRET_KEY = getenv("MADS_RAG_API_SECRET", "fallback_api_secret")

# Define fast api app
app = FastAPI()
# Define security scheme
security = HTTPBearer()
# Create ChromaDB client and get collection
database_client = chromadb.PersistentClient(path=COLLECTION_DIR)
collection = database_client.get_collection(name=COLLECTION_NAME)
# Create OpenAI client
openai_client = OpenAI()


def decode_jwt(token: str) -> Dict[str, str]:
    """
    Decode JWT token.

    Params
    ------
    - token (str): JWT token.

    Returns
    -------
    - Dict[str, Any]: Payload of the JWT token.

    """
    try:
        # Decode token using secret key
        payload: Dict[str, str] = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ENCRYPTION_ALGORITHM],
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


def authorize(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)]
) -> Dict[str, str]:
    """
    Authorize user based on JWT token.

    Params
    ------
    - credentials (HTTPAuthorizationCredentials): HTTP authorization credentials.

    Returns
    -------
    - Dict[str, Any]: Payload of the JWT token.

    """
    return decode_jwt(credentials.credentials)


class GenerationRequest(BaseModel):
    query: str


@app.post("/generate")
async def generate(
    request: GenerationRequest,
    _: Annotated[Dict[str, str], Depends(authorize)],
) -> Dict[str, str]:
    try:
        # Retrieve documents based on query
        documents: List[str] = retrieve_documents(
            collection=collection,
            query=request.query,
        )
        # Flatten documents to single context
        context = " ".join(documents)
        # Generate answer based on context and query
        answer: Dict[str, str] = generate_answer(
            client=openai_client,
            context=context,
            query=request.query,
        )
        return answer

    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
