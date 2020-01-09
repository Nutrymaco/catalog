from elasticsearch import Elasticsearch
from settings import ES_HOST, ES_PORT

es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])


# create or update
def item_index(item_id, parameters):
    es.index(index='catalog', doc_type='items', body=parameters, id=item_id)


if __name__ == "__main__":
    item_index(
        {
            "name": "new name",
            "descriptions": "fewqf"
        },
        "guh123"
    )
