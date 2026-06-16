from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

SCRAPED_DIR = "data/scraped"
CHROMA_DIR = "data/chroma_db"

def ingest():
    print("📥 Loading documents...")
    loader = DirectoryLoader(
        SCRAPED_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"   Loaded {len(documents)} documents")

    print("✂️  Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    print(f"   Created {len(chunks)} chunks")

    print("🔢 Embedding and storing in ChromaDB...")
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print(f"✅ Ingested {len(chunks)} chunks into ChromaDB at '{CHROMA_DIR}'")

if __name__ == "__main__":
    ingest()
