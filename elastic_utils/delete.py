from elasticsearch import Elasticsearch
from settings import ES_HOST, ES_PORT

es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])


def item_delete_from_elastic(item_id):
    es.delete(index='catalog', doc_type='items', id=item_id)


if __name__ == "__main__":
    item_delete_from_elastic("5e15d57ee2a1d32793f6a577")
