from typing import Dict, List, Union

import storage.mongo  # noqa: F401
from models.mongo import ScientificArticle


def search_text(keyword: str) -> list[ScientificArticle]:
    query = ScientificArticle.objects(text__icontains=keyword)
    return list(query)


def search_text_index(keyword: str) -> List[Dict[str, Union[str, float]]]:
    if not keyword.startswith('"'):
        keyword = f'"{keyword}"'

    pipeline = [
        {"$match": {"$text": {"$search": keyword}}},
        {"$addFields": {"text_score": {"$meta": "textScore"}}},
        {"$sort": {"text_score": -1}},
        {"$project": {"arxiv_id": 1, "title": 1, "text_score": 1}},
    ]

    results = list(ScientificArticle._get_collection().aggregate(pipeline))
    return results


if __name__ == "__main__":
    results = search_text("Continuous-Time Markov Chain (CTMC)")
    for article in results:
        print(f"{article.arxiv_id}:{article.title}")

    results2 = search_text_index("low-frequency correlators")
    for ar in results2:
        print(f"{ar['arxiv_id']}: {ar['title']} (score={ar['text_score']:.3f})")
