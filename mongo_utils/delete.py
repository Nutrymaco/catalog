from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT
from bson.objectid import ObjectId
from neo4j_utils.delete import delete_item_node

client = MongoClient(MONGO_HOST, MONGO_PORT)
catalog_bd = client['catalog']
items_collection = catalog_bd['items']
offers_collection = catalog_bd['offers']


def item_delete_from_mongo(doc_id):
    items_collection.delete_one({'_id': ObjectId(doc_id)})
    delete_item_node(doc_id)


def offer_delete_from_mongo(offer_id):
    offer = offers_collection.find_one({'_id': ObjectId(offer_id)})

    items_collection.update_one(
        {
            '_id': ObjectId(offer['item_id'])
        },
        {
            '$pull': {
                'offers': offer
            }
        }
    )
    item = items_collection.find_one({'_id': ObjectId(offer['item_id'])})

    offer_item = items_collection.find_one(({'_id': ObjectId(offer['item_id'])}))
    if item:
        if item['min_price'] == offer['price']:
            min_offer = min(offer_item['offers'], key=lambda offer: offer['price'])
            if not min_offer:
                items_collection.update_one({'_id': ObjectId(offer['item_id'])},
                                            {'$unset': 'min_price'})
            else:
                items_collection.update_one({'_id': ObjectId(offer['item_id'])}, {'$set': {'min_price': min_offer['price']}})

        if item['max_price'] == offer['price']:
            max_offer = max(offer_item['offers'], key=lambda offer_dict: offer_dict['price'])
            if not max_offer:
                items_collection.update_one({'_id': ObjectId(offer_item['_id'])},
                                            {'$unset': 'max_price'})
            else:
                items_collection.update_one({'_id': ObjectId(offer_item['_id'])},
                                            {'$set': {'max_price': max_offer['price']}})

    offers_collection.delete_one({'_id': ObjectId(offer_id)})


if __name__ == "__main__":
    print(offers_collection.find_one({'_id': ObjectId("5e18e7ab3dac0184747ee4f9")}))
