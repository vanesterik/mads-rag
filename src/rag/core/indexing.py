import json
from typing import List
from uuid import uuid4

import chromadb
from halo import Halo

from rag.common.config import COLLECTION_DIR, COLLECTION_NAME, CORPUS_PATH


def index_corpus(corpus: List[str]) -> None:
    """
    Index corpus in ChromaDB.

    Params
    ------
    - corpus (List[str]): List of text chunks.

    """

    # Create ChromaDB client and collection
    client = chromadb.PersistentClient(path=COLLECTION_DIR)

    # Check if collection already exists
    if COLLECTION_NAME in client.list_collections():
        # Delete collection in order to re-index
        client.delete_collection(name=COLLECTION_NAME)

    # Generate UUIDs for each document
    uuids = [str(uuid4()) for _ in range(len(corpus))]

    # Create collection and add documents
    collection = client.create_collection(name=COLLECTION_NAME)
    collection.add(documents=corpus, ids=uuids)


def load_corpus(file_path: str) -> List[str]:
    """
    Load corpus from JSON file.

    Params
    ------
    - file_path (str): Path to the JSON file.

    Returns
    -------
    - List[str]: List of text chunks

    """

    # Load JSON file
    with open(file_path, "r") as file:
        data = json.load(file)
    # Return data parsed as list of strings
    return [item for item in data]


if __name__ == "__main__":
    # Initiate and start spinner on command line
    spinner = Halo(spinner="dots")
    spinner.start(text="Indexing corpus...")

    # Index and save corpus
    corpus = load_corpus(CORPUS_PATH)
    index_corpus(corpus=corpus)

    # Finalize build process by succeeding spinner
    spinner.succeed("Build process completed")
