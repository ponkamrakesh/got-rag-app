import os
from pinecone import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from groq import Groq

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("got-index")

embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def query_rag(question):
    vec = embed_model.embed_query(question)
    results = index.query(vector=vec, top_k=5, include_metadata=True)

    context = "\n".join([m["metadata"]["text"] for m in results["matches"]])

    prompt = f"""You are a Westeros expert.\n\nContext:\n{context}\n\nQuestion:\n{question}\n"""

    res = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content