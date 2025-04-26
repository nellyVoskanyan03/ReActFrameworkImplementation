from src.react_agent.react_agent import Agent
if __name__ == "__main__":
    while True:
        query = input("Enter your question: ")
        Agent.run(query)
        if query in ["Exit", "End"]:
            break
