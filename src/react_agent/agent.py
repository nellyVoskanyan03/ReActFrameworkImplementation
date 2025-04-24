from google import genai


def run_agent(message: str):
    client = genai.Client(api_key="AIzaSyD7xy192jbZquA-bi4vCtJy3AvweL6UlK4")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[message]
    )
    print(response.text)


if __name__ == "__main__":

    print("ola")
