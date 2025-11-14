from pathlib import Path

import pandas as pd
from models.relational import Author, ScientificArticle
from sqlalchemy.exc import IntegrityError
from storage.relational_db import Session


def save_article(line: pd.Series) -> pd.Series:
    with Session() as session:
        try:
            author = Author(
                full_name=line["author_full_name"], title=line["author_title"]
            )
            article = ScientificArticle(
                title=line["title"],
                summary=line["summary"],
                file_path=line["file_path"],
                arxiv_id=line["arxiv_id"],
                author=author,
            )
            session.add(article)
            session.commit()
            session.refresh(article)
            print(f"Success: {article.arxiv_id}")
            return pd.Series([article.id, author.id], index=["db_id", "author_db_id"])
        except IntegrityError as e:
            print(f"Failure: {e}")
            return pd.Series([0, 0], index=["db_id", "author_db_id"])


def load_data_from_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(Path(path), delimiter=";", dtype="string")


def create_in_relational_db(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(save_article, axis=1)
    df = pd.concat([df, ids], axis=1)
    return df
