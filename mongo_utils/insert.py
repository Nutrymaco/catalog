from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT
from bson.dbref import DBRef
from bson.objectid import ObjectId
from mongo_utils.utils import change_item_price

client = MongoClient(MONGO_HOST, MONGO_PORT)
catalog_bd = client['catalog']
items_collection = catalog_bd['items']
offers_collection = catalog_bd['offers']


def item_insert(parameters):
    return items_collection.insert_one(parameters).inserted_id


def offer_insert(parameters):
    parameters['item_id'] = ObjectId(parameters['item_id'])
    offer = offers_collection.insert_one(parameters)
    offer_id = offer.inserted_id
    offer_item_id = parameters['item_id']
    offer_price = parameters['price']


    change_item_price(items_collection, offer_item_id, offer_price)
    del parameters['item_id']
    items_collection.update_one({'_id': offer_item_id},
                                {'$push': {
                                    'offers': parameters
                                }})


def item_exists(parameters):
    return bool(items_collection.count_documents(parameters))


if __name__ == "__main__":
    mvideo = {
            "name": "Macbook air 2018 new 128 gb",
            "url": "https://mvideo.ru/electronics/laptops/macbook-air-2018-128gb",
            "item_id": "5e15d89d7dcd01fcbf837fb0",
            "price": 1000,
            "old_price": 1000,
            "discount": False,
            "currency": "dollar",
            "count": 2000,
            "refurbished": False,
            "delivery": True,
            "delivery_price": 150,
            "delivery_time": "1",
            "pickup": True,
            "pickup_price": 0,
            "pickup_time": "0"
        }
    citilink = {
        "name": "Macbook air 2018 new 128 gb",
        "url": "https://mvideo.ru/electronics/laptops/macbook-air-2018-128gb",
        "item_id": "5e15d89d7dcd01fcbf837fb0",
        "price": 900,
        "old_price": 900,
        "discount": False,
        "currency": "dollar",
        "count": 3000,
        "refurbished": False,
        "delivery": True,
        "delivery_price": 250,
        "delivery_time": "1",
        "pickup": False
      }

    mvideo1 = {
        "name": "Ipad 4 128 gb",
        "url": "https://mvideo.ru/electronics/laptops/macbook-air-2018-128gb",
        "item_id": "5e15d8a87dcd01fcbf837fb1",
        "price": 500,
        "old_price": 500,
        "discount": False,
        "currency": "dollar",
        "count": 2000,
        "refurbished": False,
        "delivery": True,
        "delivery_price": 150,
        "delivery_time": "1",
        "pickup": True,
        "pickup_price": 0,
        "pickup_time": "0"
      }
    citilink1 = {
        "name": "Ipad 4 128 gb",
        "url": "https://mvideo.ru/electronics/laptops/macbook-air-2018-128gb",
        "item_id": "5e15d8a87dcd01fcbf837fb1",
        "price": 450,
        "old_price": 450,
        "discount": False,
        "currency": "dollar",
        "count": 2000,
        "refurbished": False,
        "delivery": True,
        "delivery_price": 150,
        "delivery_time": "1",
        "pickup": False
      }

    offer_insert(citilink1)


