from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import pandas as pd
import requests
import storage.mongo  # noqa: F401
from bs4 import BeautifulSoup
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from mongoengine import DoesNotExist


def extract_text_from_html(html_content: str) -> str:
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.find("body")
    text = body.get_text(separator="\n") if body else soup.get_text(separator="\n")
    return text  # type: ignore[no-any-return]


def download_file(article: pd.Series) -> pd.Series:
    parsed_url = urlparse(article.file_path)
    if parsed_url.scheme:
        filename = Path(parsed_url.path).name
        new_path = f"data/papers/{filename}.pdf"
        if not Path(new_path).exists():
            response = requests.get(article.file_path)
            with open(new_path, "wb") as f:
                f.write(response.content)
    else:
        new_path = article.file_path

    return pd.Series([new_path], index=["local_file_path"])


def save_article(article: pd.Series) -> pd.Series:
    try:
        m_author = MongoAuthor(
            db_id=article.author_db_id,
            full_name=article.author_full_name,
            author_title=article.author_title,
        )
        text_content_from_html = extract_text_from_html(article.html_content)
        kwargs = dict(
            db_id=article.db_id,
            title=article.title,
            summary=article.summary,
            file_path=article.file_path,
            arxiv_id=article.arxiv_id,
            author=m_author,
            text=text_content_from_html,
        )
        try:
            m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            m_article.update(**kwargs)
        except DoesNotExist:
            m_article = MongoArticle(**kwargs)
            m_article.save()

        print(f"Success: {article.arxiv_id}")
        mongo_db_id: str = str(m_article.id)
        return pd.Series([mongo_db_id], index=["mongo_db_id"])
    except Exception as e:
        print(f"Failure: {e}")
        return pd.Series([""], index=["mongo_db_id"])


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(save_article, axis=1)
    df = pd.concat([df, ids], axis=1)
    return df


def download_files(df: pd.DataFrame) -> pd.DataFrame:
    filenames = df.apply(download_file, axis=1)
    df = pd.concat([df, filenames], axis=1)
    return df


def download_html_article(row: pd.Series) -> Optional[str]:
    try:
        response = requests.get(row["arxiv_id"])
        response.raise_for_status()
        return response.text  # type: ignore[no-any-return]
    except Exception as e:
        print(f"No existing arxiv_id: {row['arxiv_id']}: {e}")
        return None


def add_html_content(df: pd.DataFrame) -> pd.DataFrame:
    df["html_content"] = df.apply(download_html_article, axis=1)
    return df
