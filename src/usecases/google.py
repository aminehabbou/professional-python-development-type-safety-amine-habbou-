import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)


def apply_chunking(
    article: pd.Series, chunk_size: int = 1000, overlap: int = 200
) -> pd.Series:
    text = article.html_content
    start = 0
    chunks: list[str] = []
    while start < len(article.html_content):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return pd.Series([chunks, range(len(chunks))], index=["chunk_text", "chunk_index"])


def embed_article(article_chunk: pd.Series) -> pd.Series:
    if article_chunk.exists_in_qdrant:
        return pd.Series([None], index=["embedding"])
    if article_chunk.chunk_index >= 2:  # due to quota limit has been exceeded
        return pd.Series([None], index=["embedding"])

    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[article_chunk.chunk_text],
        config=types.EmbedContentConfig(
            output_dimensionality=768, task_type="RETRIEVAL_DOCUMENT"
        ),
    )

    if result.embeddings is None:
        return pd.Series([None], index=["embedding"])

    return pd.Series([np.array(result.embeddings[0].values)], index=["embedding"])


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    results = df.apply(embed_article, axis=1)
    df = pd.concat([df, results], axis=1)
    return df


def chunk_documents(df: pd.DataFrame) -> pd.DataFrame:
    chunks = df.apply(apply_chunking, axis=1)
    return pd.concat([df, chunks], axis=1).explode(["chunk_index", "chunk_text"])
