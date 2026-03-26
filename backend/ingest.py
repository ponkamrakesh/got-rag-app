import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone


def ingest():
    loader = PyPDFLoader("data/got.pdf")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("got-index")

    vectors = []
    for i, chunk in enumerate(chunks):
        vec = embeddings.embed_query(chunk.page_content)
        vectors.append((f"id-{i}", vec, {"text": chunk.page_content}))

    index.upsert(vectors)


if __name__ == "__main__":
    ingest()
