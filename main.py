from rag.query import load_rag_chain, ask

def main():
    print("=" * 50)
    print("🎓 CampusBuddy - AIET Campus Assistant")
    print("   Type 'exit' to quit")
    print("=" * 50)

    print("\n⏳ Loading CampusBuddy RAG engine...")
    chain = load_rag_chain()
    print("✅ CampusBuddy is ready!\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "bye"]:
            print("CampusBuddy: Goodbye! Have a great day! 👋")
            break
        if not question:
            continue
        print("CampusBuddy: ", end="", flush=True)
        answer = ask(chain, question)
        print(answer)
        print()

if __name__ == "__main__":
    main()
