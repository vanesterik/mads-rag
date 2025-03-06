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

    # Generate UUIDs for each document
    uuids = [str(uuid4()) for _ in range(len(corpus))]

    # Create ChromaDB client and collection with local Hugging Face model
    client = chromadb.PersistentClient(path=COLLECTION_DIR)
    collection = client.create_collection(name=COLLECTION_NAME)

    # Add documents to collection
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
