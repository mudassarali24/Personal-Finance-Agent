from src.agent import create_finance_agent

def main():
    print("=" * 60)
    print("Personal Finance Agent")
    print("=" * 60)
    print("\nInitializing agent...")

    try:
        agent = create_finance_agent()
        print("Agent ready!")
        print("Type 'quit' or 'exit' to stop")

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nTerminated!")
                break

            if not user_input:
                continue

            try:
                response = agent.invoke({"input": user_input})
                print(f"\nAgent: {response['output']}")
            except Exception as e:
                print(f"\n Error: {e}")

    except Exception as e:
        print(f"\nError: {e}")
        return
    
if __name__ == "__main__":
    main()