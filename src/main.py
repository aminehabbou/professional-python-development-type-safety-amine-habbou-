from usecases.export_articles import create_in_mongo
from usecases.import_articles import create_in_relational_db, load_data_from_csv
from usecases.search_text import search_text_index

if __name__ == "__main__":
    df = (
        load_data_from_csv("data/articles.csv")
        .pipe(create_in_relational_db)
        .pipe(create_in_mongo)
    )
    print("DataFrame after importing to relational db and exporting to mongo:")
    print(df)

    results = search_text_index("low-frequency correlators")
    print("len results:", len(results))
    for ar in results:
        print(f"{ar['arxiv_id']}: {ar['title']} (score={ar['text_score']:.3f})")
