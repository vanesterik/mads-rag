# MADS RAG

## Introduction

This repository contains the code for the [MADS](https://www.hanuniversity.com/en/programs/master/applied-data-science/parttime/) RAG project. The project consists of a [ChromaDB](https://docs.trychroma.com/docs/overview/introduction) database and server running in a [Docker](https://www.docker.com/) container. The database is populated with the extraction of the main books master of applied data science education.

The idea is to use the server to retrieve documents from the database and use these for a RAG model (of your own choice) to generate answers to questions.

## Requirements

- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)
- [PDM](https://pdm-project.org/)


## Usage

To build the database, run the following command:

```bash
make build
```

To test a predetermined retrieval of the database, run the following command (see `src/core/retrieving.py` for more details):

```bash
make run
```

To run the server, run the following command:

```bash
docker compose up -d
```

All usual Docker commands can be used to manage the container. To stop the server, run the following command:

```bash
docker compose down
```

## References

- [ChromaDB](https://docs.trychroma.com/docs/overview/introduction)
- [Docker](https://www.docker.com/)
- [MADS](https://www.hanuniversity.com/en/programs/master/applied-data-science/parttime/)
- [PDM](https://pdm-project.org/)
- [Python](https://www.python.org/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



