import json
import os
import re
from typing import Dict, List, Tuple

import pdfplumber
from halo import Halo
from pypdf import PdfReader

from rag.common.config import CORPUS_PATH, DOCUMENT_DIR


def extract_page_elements(file_path: str) -> Tuple[List[str], List[str]]:
    """
    Extract page elements (headers and footers) from a list of PDF pages:

        - Get all headers from the page based on the font style. This might not
          work for all documents and should be adjusted accordingly.
        - Get all footers from the page based on the position of the text.

    Note that a distinction is made between white and black color of the text.
    White text is most likely part of a table header and should not be
    considered as a header.

    Params
    ------
    - pages (List[PageObject]): List of PDF pages.

    Returns
    -------
    - Tuple[List[str], List[str]]: Tuple containing headers and footers.

    """

    # Define empty lists to hold headers and footers
    headers: List[str] = []
    footers: List[str] = []

    with pdfplumber.open(file_path) as document:

        for page in document.pages:
            # Process page to get all header-like elements based on font style
            # and color of the text (non-white)
            words = page.extract_words(
                extra_attrs=[
                    "fontname",
                    "non_stroking_color",
                ]
            )
            lines: Dict[float, List[str]] = {}

            for word in words:
                if (
                    "Semibold" in word["fontname"]
                    and word["non_stroking_color"] != (1,)
                    and word["non_stroking_color"] != (1, 1, 1)
                ):
                    line_num = word["top"]

                    if line_num not in lines:
                        lines[line_num] = []

                    lines[line_num].append(word["text"])

            for line in lines.values():
                headers.append(" ".join(line))

            # Process page to get all footer elements based on the position of
            # the text (bottom of the page)
            footer_threshold = page.height * 0.1
            bottom_margin = page.height - footer_threshold

            footer = [
                word["text"]
                for word in page.extract_words()
                if word["top"] > bottom_margin
            ]
            footers.append(" ".join(footer))

            # Sanitize headers and footers
            footers = [footer for footer in footers if footer.strip() != ""]
            headers = [header for header in headers if header not in footers]

    return (headers, footers)


def extract_chunks(file_path: str, headers: List[str], footers: List[str]) -> List[str]:
    """
    Extract text chunks from a PDF file based on headers and footers:

        - Extract text from all pages in the PDF file.
        - Remove all footers from the text.
        - Split text into chunks using headers pattern.
        - Sanitize chunks by removing empty strings and headers.

    Params
    ------
    - file_path (str): Path to the PDF file.
    - headers (List[str]): List of headers.
    - footers (List[str]): List of footers.

    Returns
    -------
    - List[str]: List of text chunks.

    """

    # Define empty list to hold all text chunks
    chunks: List[str] = []

    # Extract text from pages
    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages])

    # Remove all footers from text
    for footer in footers:
        text = text.replace(footer, "")

    # Define headers pattern
    headers_pattern = "|".join(map(re.escape, headers))

    # Split text into chunks using headers pattern
    chunks = re.split(f"\n({headers_pattern})\n", text)

    # Sanitize chunks
    chunks = [chunk for chunk in chunks if chunk.strip() != ""]
    chunks = [chunk for chunk in chunks if chunk not in headers]
    chunks = [chunk.replace("\n", " ").strip() for chunk in chunks]

    return chunks


def extract_corpus(dir: str) -> List[str]:
    """
    Extract corpus from a directory containing PDF files:

        - Loop through all files in the directory.
        - Extract headers and footers from each file.
        - Extract text chunks from each file based on headers and footers.
        - Append chunks to corpus list.

    Params
    ------
    - dir (str): Path to the directory containing PDF files.

    Returns
    -------
    - List[str]: List of text chunks.

    """

    # Define empty list to hold all document chunks
    corpus: List[str] = []

    # Loop through all files in the directory
    for file in os.listdir(dir):

        # Skip file it is not a PDF
        if not file.endswith(".pdf"):
            continue

        # Extract required elements from file
        file_path = os.path.join(dir, file)
        headers, footers = extract_page_elements(file_path)
        chunks = extract_chunks(file_path, headers, footers)

        # Append chunks to corpus list
        corpus.extend(chunks)

    return corpus


def save_corpus(file_path: str, corpus: List[str]) -> None:
    """
    Save corpus to a JSON file.

    Params
    ------
    - file_path (str): Path to the JSON file.
    - corpus (List[str]): List of text chunks.

    """

    with open(file_path, "w") as file:
        json.dump(corpus, file)


if __name__ == "__main__":
    # Initiate and start spinner on command line
    spinner = Halo(spinner="dots")
    spinner.start(text="Extracting corpus...")

    # Extract and save corpus
    corpus = extract_corpus(dir=DOCUMENT_DIR)
    save_corpus(file_path=CORPUS_PATH, corpus=corpus)

    # End by stopping spinner
    spinner.stop()
