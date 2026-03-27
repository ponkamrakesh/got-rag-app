from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pinecone
from config import *

def ingest_pdf(pdf_path="got.pdf"):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    model = SentenceTransformer(EMBED_MODEL)

    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts)

    pinecone.init(api_key=PINECONE_API_KEY)
    index = pinecone.Index(INDEX_NAME)

    to_upsert = [
        (str(i), embeddings[i].tolist(), {"text": texts[i]})
        for i in range(len(texts))
    ]

    index.upsert(vectors=to_upsert)

    print("PDF ingested into Pinecone")

ingest_pdf()
