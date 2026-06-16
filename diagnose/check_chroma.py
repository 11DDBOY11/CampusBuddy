# check_chroma.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="data/chroma_db", embedding_function=embeddings)

results = db.similarity_search("CSC branch", k=5)
for i, doc in enumerate(results):
    print(f"\n--- Chunk {i+1} ---")
    print(doc.page_content[:300])