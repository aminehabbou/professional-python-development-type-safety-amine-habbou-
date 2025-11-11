import storage.mongo  # noqa: F401
from models.mongo import ScientificArticle

indexes = ScientificArticle._get_collection().index_information()
print(indexes)
