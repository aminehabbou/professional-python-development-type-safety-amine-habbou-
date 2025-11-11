import pymupdf4llm
import storage.mongo  # noqa: F401
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from models.relational import ScientificArticle
from mongoengine import DoesNotExist
from sqlalchemy import select
from storage.relational_db import Session


def export_from_db() -> None:
    with Session() as session:
        query = select(ScientificArticle)
        result = session.execute(query)
        for article in result.scalars().all():
            m_author = MongoAuthor(
                db_id=article.author.id,
                full_name=article.author.full_name,
                author_title=article.author.title,
            )
            md_text = pymupdf4llm.to_markdown(article.file_path)
            try:
                m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
                m_article.update(
                    db_id=article.id,
                    title=article.title,
                    summary=article.summary,
                    file_path=article.file_path,
                    created_at=article.created_at,
                    arxiv_id=article.arxiv_id,
                    author=m_author,
                    text=md_text,
                )
            except DoesNotExist:
                m_article = MongoArticle(
                    db_id=article.id,
                    title=article.title,
                    summary=article.summary,
                    file_path=article.file_path,
                    created_at=article.created_at,
                    arxiv_id=article.arxiv_id,
                    author=m_author,
                    text=md_text,
                )
                m_article.save()


if __name__ == "__main__":
    export_from_db()
