from typing import List

from chromadb import Collection, HttpClient

from rag.common.config import COLLECTION_NAME, TOP_K


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


if __name__ == "__main__":
    # Create ChromaDB client and collection
    client = HttpClient(host="localhost", port=8000)
    collection = client.get_collection(name=COLLECTION_NAME)

    # Query documents
    query = "What is machine learning?"
    documents = retrieve_documents(collection=collection, query=query)

    # Print retrieved documents
    print(documents)
