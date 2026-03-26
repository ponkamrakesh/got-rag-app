import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

INDEX_NAME = "got-chatbot"
EMBED_MODEL = "all-MiniLM-L6-v2"