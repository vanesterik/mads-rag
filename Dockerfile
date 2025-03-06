FROM chromadb/chroma:latest

# Ensure the database directory exists
RUN mkdir -p /chroma

# Set working directory to ChromaDB storage
WORKDIR /chroma

# Set database directory as a volume
VOLUME ["/chroma"]
