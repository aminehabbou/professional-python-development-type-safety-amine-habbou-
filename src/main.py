from usecases.arxiv import fetch_arxiv_articles
from usecases.export_articles import (
    add_html_content,
    create_in_mongo,
    download_files,
)
from usecases.google import chunk_documents, embed_documents
from usecases.import_articles import create_in_relational_db
from usecases.qdrant import check_chunks_in_qdrant, save_to_qdrant
from usecases.search_text import search_text_index

if __name__ == "__main__":
    df = (
        fetch_arxiv_articles("quantum")
        .pipe(create_in_relational_db)
        .pipe(download_files)
        .pipe(add_html_content)
        .pipe(chunk_documents)
        .pipe(check_chunks_in_qdrant)
        .pipe(embed_documents)
        .pipe(save_to_qdrant)
        .pipe(create_in_mongo)
    )
    print("DataFrame after (relational DB insertion and export to mongodb):")
    print(df)

    print(f"Total chunks: {len(df)}")
    print(f"Chunks with embeddings: {df['embedding'].notna().sum()}")
    print(f"Chunks without embeddings: {df['embedding'].isna().sum()}")

    results = search_text_index("quantum entanglement")
    print("len results:", len(results))
    for article in results:
        print(f"{article['arxiv_id']}: {article['title']}")
