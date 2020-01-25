from elasticsearch import Elasticsearch
from settings import ES_HOST, ES_PORT

es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])


def search_items_from_elastic(text, only_id=False):
    body = {
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": text,
                        "type": "most_fields",
                        "fields": [
                            "name^3",
                            "description^2"
                        ],
                        "fuzziness": "AUTO",
                        "prefix_length": 2
                    }
                }
            }
        },
        "_source": ["_id", "_score", 'id']
    }

    items = es.search(index='catalog', body=body)["hits"]["hits"]

    if only_id:
        id_list = [item['_id'] for item in items]
        return id_list
    return items


if __name__ == "__main__":
    print(search_items_from_elastic("air"))