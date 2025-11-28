from qdrant_client.models import ScoredPoint
from storage.qdrant import COLLECTION_NAME, client
from utils.embed import embed
from utils.timeit import timeit


@timeit("Search qdrant")
def search_qdrant(query: str) -> list[ScoredPoint]:
    query_vector = embed(query, task_type="RETRIEVAL_QUERY")
    results = client.query_points(COLLECTION_NAME, query_vector, with_payload=True)
    return results.points


if __name__ == "__main__":
    results = search_qdrant(
        " How do humans routinely solve problems of immense computational complexity?"
    )
    for point in results:
        chunk_text = (point.payload or {})["chunk_text"]
        print(f"Score: {point.score}\n{chunk_text}")
        print("-" * 50)
