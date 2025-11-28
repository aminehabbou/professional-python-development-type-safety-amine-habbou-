import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)


models = client.models.list()
for model in models:
    print(f"Model: {model.name}")
    print(f"Display name: {model.display_name}")
    print(f"Description: {model.description}")
    print("---")
