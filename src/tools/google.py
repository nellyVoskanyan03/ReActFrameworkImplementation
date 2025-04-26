from typing import Any
import json
import requests
import os
from pathlib import Path
from typing import List
from typing import Dict
from typing import Union
from typing import Tuple

CREDENTIALS_PATH = Path(__file__).parent.parent / 'credentials/key.json'


class SerpAPIClient:

    def __init__(self, api_key: str):

        self.api_key = api_key
        self.base_url = "https://serpapi.com/search.json"

    def __call__(self, query: str, engine: str = "google", location: str = "") -> Union[Dict[str, Any], Tuple[int, str]]:

        params = {
            "engine": engine,
            "q": query,
            "api_key": self.api_key,
            "location": location
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request to SERP API failed: {e}")
            return response.status_code, str(e)


def format_top_search_results(results: Dict[str, Any], top_n: int = 10) -> List[Dict[str, Any]]:

    return [
        {
            "position": result.get('position'),
            "title": result.get('title'),
            "link": result.get('link'),
            "snippet": result.get('snippet')
        }
        for result in results.get('organic_results', [])[:top_n]
    ]


def load_serp_key():
    with open(CREDENTIALS_PATH, 'r') as file:
        data = json.load(file)
        return data["serp"]["key"]


def search(search_query: str, location: str = "") -> str:

    serp_client = SerpAPIClient(load_serp_key())

    results = serp_client(search_query, location=location)

    if isinstance(results, dict):
        top_results = format_top_search_results(results)
        return json.dumps({"top_results": top_results}, indent=2)
    else:
        status_code, error_message = results
        error_json = json.dumps(
            {"error": f"Search failed with status code {status_code}: {error_message}"})
        print(error_json)
        return error_json


if __name__ == "__main__":
    search_query = "Best gyros in Barcelona, Spain"
    result_json = search(search_query, '')
    print(result_json)
