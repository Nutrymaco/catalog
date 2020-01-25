from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT
from pymongo.collection import ObjectId
from mongo_utils.utils import transform_to_mongo_language

client = MongoClient(MONGO_HOST, MONGO_PORT)
catalog_bd = client['catalog']
items_collection = catalog_bd['items']
offers_collection = catalog_bd['offers']


def get_elements_from_mongo(collection_name, parameters=None, document_ids=None, only_one=False):
    parameters_for_find = {}
    if parameters:
        parameters_for_find = transform_to_mongo_language(parameters)
        if collection_name == 'items':
            if 'price' in parameters:
                if type(parameters['price']) == list:
                    parameters_for_find['$or'] = [
                        {'min_price': {'$lte': parameters['price'][1]}},
                        {'max_price': {'$gte': parameters['price'][0]}}
                    ]
                else:
                    parameters_for_find['min_price'] = {
                        '$lte': parameters['price']
                    }
                    parameters_for_find['max_price'] = {
                        '$gte': parameters['price']
                    }
                del parameters['price']
                del parameters_for_find['price']

    if document_ids:
        parameters_for_find['_id'] = {
            '$in': [ObjectId(document_id) for document_id in document_ids]
        }
    if only_one:
        print(parameters_for_find)
        item = catalog_bd[collection_name].find_one(parameters_for_find)
        if not item:
            return {}
        item['id'] = str(item['_id'])
        del item['_id']
        # да, это очень плохо, но пока хз как лучше сделать
        if 'item_id' in item:
            item['item_id'] = str(item['item_id'])
        if 'offers' in item:
            for offer in item['offers']:
                offer['id'] = str(offer['_id'])
                del offer['_id']
        return item
    else:
        items = list(catalog_bd[collection_name].find(parameters_for_find))

    for item in items:
        item['id'] = str(item['_id'])
        if 'offers' in item:
            for offer in item['offers']:
                offer['id'] = str(offer['_id'])
                del offer['_id']
        del item['_id']
    return items


# optimized by denormalized sheme
def get_offer_from_mongo(parameters=None):
    if parameters:
        if 'item_id' in parameters:
            item = items_collection.find_one({'_id': ObjectId(parameters['item_id'])})
            offers = item['offers']
            if len(parameters.keys()) == 1:
                return offers
            else:
                del parameters['item_id']
                parameters_for_find = transform_to_mongo_language(parameters)
                parameters_for_find['_id'] = {
                            '$in': [doc['_id'] for doc in offers]
                        }
                offers = offers_collection.find(parameters_for_find)
        else:
            parameters_for_find = transform_to_mongo_language(parameters)
            offers = offers_collection.find(parameters_for_find)
    else:
        offers = offers_collection.find({})

    return list(offers)


if __name__ == "__main__":
    test_parameters = {
        'parameter_name': 'value',
        'parameter_with_range_name': ('min_value', 'max_value')
    }

    item = get_elements_from_mongo('items', document_ids=["5e15d89d7dcd01fcbf837fb0"], only_one=True)

