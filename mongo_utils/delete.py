from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT
from bson.objectid import ObjectId

client = MongoClient(MONGO_HOST, MONGO_PORT)
catalog_bd = client['catalog']
items_collection = catalog_bd['items']
offers_collection = catalog_bd['offers']


def item_delete_from_mongo(doc_id):
    items_collection.delete_one({'_id': ObjectId(doc_id)})


def offer_delete_from_elastic(offer_id):
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
    offers_collection.delete_one({'_id': ObjectId(offer_id)})


if __name__ == "__main__":
    item_delete_from_mongo("5e15d9177dcd01fcbf837fb3")