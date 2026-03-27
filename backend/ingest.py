from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pinecone
from config import *

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks
def upsert_in_batches(index, vectors, batch_size=100):
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)

def ingest_pdf(pdf_path="got.pdf"):
    reader = PdfReader("/kaggle/input/datasets/rakeshponkam/got-westeros/got.pdf")
    c=1
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
        if c%200 ==0:
            print("page no : ",c)
        c+=1
    print("PDF loaded")
    texts = chunk_text(text)
    print("Chunks:", len(texts))
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
    embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True)
    print("Embeddings done on:", device)

    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index_name = "got-chatbot"
    if index_name not in [i.name for i in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    index = pc.Index(index_name)
    
    vectors = [
    {
        "id": str(i),
        "values": embeddings[i].tolist(),
        "metadata": {"text": texts[i][:500]}  # optional trim
    }
    for i in range(len(texts))
]  
    upsert_in_batches(index, vectors)
    print("PDF ingested into Pinecone")

ingest_pdf()
