from agent import run_agent

if __name__ == "__main__":
    while True:
        cmd = input("\nEnter command: ")

        if cmd.lower() in ["exit", "quit"]:
            break

        run_agent(cmd)