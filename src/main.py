from pathlib import Path

from usecases.export_articles import export_from_db
from usecases.import_articles import load_data_from_csv
from usecases.search_text import search_text_index

if __name__ == "__main__":
    load_data_from_csv(Path("data/articles.csv"))
    export_from_db()
    results = search_text_index("low-frequency correlators")
    for ar in results:
        print(f"{ar['arxiv_id']}: {ar['title']} (score={ar['text_score']:.3f})")
