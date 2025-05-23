from typing import Optional
import wikipediaapi
import json


def search(query: str) -> Optional[str]:
    wiki = wikipediaapi.Wikipedia(user_agent='ReAct Agents (voskanyannelli03@gmail.com)',
                                  language='en')

    try:
        print(f"Searching Wikipedia for: {query}")
        page = wiki.page(query)

        if page.exists():
            result = {
                "query": query,
                "title": page.title,
                "summary": page.summary
            }
            print(f"Successfully retrieved summary for: {query}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        else:
            print(f"No results found for query: {query}")
            return None

    except Exception as e:
        print(
            f"An error occurred while processing the Wikipedia query: {e}")
        return None


if __name__ == '__main__':
    queries = ["sun", "moon"]

    for query in queries:
        result = search(query)
        if result:
            print(f"JSON result for '{query}':\n{result}\n")
        else:
            print(f"No result found for '{query}'\n")
