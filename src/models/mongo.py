from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    StringField,
)


class Author(EmbeddedDocument):  # type: ignore[misc]
    id = IntField(required=True)
    full_name = StringField()
    authot_title = StringField()


class ScientificArticle(Document):  # type: ignore[misc]
    id = IntField(required=True)
    title = StringField()
    summary = StringField()
    file_path = StringField()
    created_at = DateTimeField()

    arxiv_id = StringField()

    author = EmbeddedDocumentField(Author)

    text = StringField()
