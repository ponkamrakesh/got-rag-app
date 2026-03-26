import pinecone
from sentence_transformers import SentenceTransformer
from groq import Groq
from config import *

model = SentenceTransformer(EMBED_MODEL)
client = Groq(api_key=GROQ_API_KEY)

pinecone.init(api_key=PINECONE_API_KEY)
index = pinecone.Index(INDEX_NAME)

def retrieve_context(query, top_k=3):
    q_emb = model.encode([query])[0]

    results = index.query(
        vector=q_emb.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    return "\n".join([match["metadata"]["text"] for match in results["matches"]])


def generate_answer(query):
    context = retrieve_context(query)

    prompt = f"""
You are a Game of Thrones expert.

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content