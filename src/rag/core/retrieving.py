from typing import List

from chromadb import Collection

from rag.common.config import TOP_K


def retrieve_documents(collection: Collection, query: str) -> List[str]:
    """
    Retrieve documents from a collection based on a query.

    Params
    ------
    - collection (Collection): ChromaDB collection.
    - query (str): Query to retrieve documents.

    """

    # Query results from collection
    results = collection.query(query_texts=[query], n_results=TOP_K)

    # For some reason, the documents within the results are nested
    documents = results["documents"][0]

    # Extract documents from results
    return [document for document in documents]
