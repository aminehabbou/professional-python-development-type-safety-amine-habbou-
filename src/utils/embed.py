import os
from typing import Any

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)


def embed(text: str, task_type: str) -> np.ndarray[Any, np.dtype[np.float32]]:
    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[text],
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type=task_type,
        ),
    )
    if result.embeddings is None:
        raise ValueError

    return np.array(result.embeddings[0].values)
