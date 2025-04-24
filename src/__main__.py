from react_agent import run_agent
if __name__ == "__main__":
    while True:
        query = input("Enter your question: ")
        run_agent(query)
        if query in ["Exit", "End"]:
            break
