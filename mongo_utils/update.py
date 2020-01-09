from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT
from pymongo.collection import ObjectId
from .utils import change_item_price

client = MongoClient(MONGO_HOST, MONGO_PORT)
catalog_bd = client['catalog']
items_collection = catalog_bd['items']
offer_collection = catalog_bd['offers']
offers_collection = catalog_bd['offers']


def item_update_in_mongo(item_id, parameters):
    items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": parameters})


def offer_update_in_mongo(offer_id, parameters):
    offer = offers_collection.find_one({'_id': ObjectId(offer_id)})
    offer_item_id = offer['item_id']
    if 'price' in parameters:
        offer_price = parameters['price']
        change_item_price(items_collection, offer_item_id, offer_price)

    items_collection.update_one({'_id': ObjectId(offer_item_id), '$pull': {'offers': offer}})
    new_offer = offer_collection.update_one(
        {
            '_id': ObjectId(offer_id)
        },
        {
            '$set': parameters
        }
    )
    items_collection.update_one({'_id': ObjectId(offer_item_id), '$push': {'offers': new_offer}})


if __name__ == "__main__":
    print(items_collection.find_one(
        filter={
            "_id": ObjectId("5e1613c790bb4561d4155d15")
        }
    ))
    item_update_in_mongo("5e1613c790bb4561d4155d15",
                         {
                             "name": "ipaaaad",
                             "OS": "IOS 12"
                         }
    )
