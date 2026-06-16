from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

CHROMA_DIR = "data/chroma_db"

PROMPT_TEMPLATE = """
You are CampusBuddy, a helpful and friendly AI assistant for Alva's Institute of Engineering and Technology (AIET), Moodubidri.

Use only the context below to answer the question in simple spoken English.
Answer naturally, clearly, and helpfully.
Do not mention URLs, website links, file names, or source names.
Do not say "based on the provided context".
Focus on factual college information only.
Do NOT repeat alumni testimonials or personal experiences.
If the answer is not fully available, say that clearly in one short sentence, then give the closest useful information from the context.
If the context does not contain the answer, say: "I could not find the exact information about that." and stop.
Keep the answer concise, natural, and suitable for voice output.

Context:
{context}

Question: {question}

Answer:
"""

def load_rag_chain():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    llm = OllamaLLM(
        model="llama3.2:1b",
        temperature=0.1,
        num_ctx=2048,
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        if not docs:
            return "No relevant information found."
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def ask(chain, question):
    return chain.invoke(question)