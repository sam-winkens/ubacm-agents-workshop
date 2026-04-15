# main.py
# Entry point. Run this file to start chatting with the agent system.
#
#   python main.py
#
# Type a message and press Enter. Press Ctrl+C to quit.

from master_agent import master_agent


def main():
    print("Multi-Agent Demo — type a message to get started. (Ctrl+C to quit)\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        response = master_agent(user_input)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
