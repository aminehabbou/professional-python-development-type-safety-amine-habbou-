import os

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

results = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[
        "a goal is scored in the net of the opposing team",
        "the opposing team conceded a goal",
        "the goal scored was a header",
        "Football is a game that consists of goals",
        "Jules kounde is a FC barcelona  football player",
        "Prague is the capital of Czech Republic",
    ],
    config=types.EmbedContentConfig(
        output_dimensionality=768, task_type="SEMANTIC_SIMILARITY"
    ),
)

embeddings_matrix = np.array(
    [np.array(embedding.values) for embedding in results.embeddings or []]
)

print(embeddings_matrix)

similarity_matrix = cosine_similarity(embeddings_matrix)

print(similarity_matrix)
