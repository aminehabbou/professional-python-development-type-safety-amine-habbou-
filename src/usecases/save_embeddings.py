import json

import pandas as pd


def save_embeddings_to_file(
    df: pd.DataFrame, filename: str = "data/embeddings.json"
) -> None:
    embeddings_data = {}
    for i, row in df.iterrows():
        embeddings_data[row["arxiv_id"]] = {
            "title": row["title"],
            "embeddings": row["embeddings"].tolist(),
        }
    with open(filename, "w") as f:
        json.dump(embeddings_data, f)
