import os
import json
from google import genai
from pathlib import Path

CREDENTIALS_PATH = Path(__file__).parent.parent / 'credentials/key.json'


def set_gemini_key():
    try:
        with open(CREDENTIALS_PATH, 'r') as file:
            data = json.load(file)
            api_key = data.get("gemini", {}).get("key")
            if not api_key:
                raise ValueError(
                    "Gemini API key is missing in the credentials file.")
            os.environ["GOOGLE_API_KEY"] = api_key
            print("Gemini API key set successfully.")
    except FileNotFoundError:
        print(f"Credentials file not found at {CREDENTIALS_PATH}.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error reading credentials file: {e}")
        raise
    except ValueError as e:
        print(e)
        raise


def get_model():
    set_gemini_key()

    try:
        client = genai.Client()
        return client.models
    except Exception as e:
        print(f"Failed to get Gemini models: {e}")
        return None


def generate(model, contents):
    try:
        print("Generating response from Gemini...")

        response = model.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config={
                "temperature": 0.5,
                "top_p": 1.0,
                "top_k": 40,
                "max_output_tokens": 20000,
                "stop_sequences": ["\n\n"],
            }
        )

        if not response.text:
            print("Empty response from the model.")
            return None

        print("Successfully generated response.")
        return response.text

    except Exception as e:
        print(f"Error generating response from Gemini: {e}")
        return None
