from pymongo.collection import ObjectId


def transform_to_mongo_language(parameters):
    return {key: parameters[key] if type(parameters[key]) is not list else
    {'$gte': parameters[key][0], '$lte': parameters[key][1]} for key in parameters}


def change_item_price(items_collection, shop_offer_item_id, shop_offer_price):
    # изменение минимальной и максимальной цены
    if items_collection.find_one(
            {'_id': ObjectId(shop_offer_item_id), 'min_price': {'$exists': False}, 'max_price': {'$exists': False}}):
        items_collection.update_one(
            {
                '_id': ObjectId(shop_offer_item_id),
                'min_price': {
                    '$exists': False
                },
            },
            {
                '$set': {
                    'min_price': shop_offer_price,
                    'max_price': shop_offer_price
                }
            }
        )
    elif items_collection.find_one(
            {'_id': ObjectId(shop_offer_item_id), 'min_price': {'$gt': shop_offer_price}}):
        items_collection.update_one(
            {
                '_id': ObjectId(shop_offer_item_id),
                'min_price': {
                    '$gt': shop_offer_price
                }
            },
            {
                '$set': {
                    'min_price': shop_offer_price
                }
            }
        )

    elif items_collection.find_one(
            {'_id': ObjectId(shop_offer_item_id), 'max_price': {'$lt': shop_offer_price}}):
        items_collection.update_one(
            {
                '_id': ObjectId(shop_offer_item_id),
                'max_price': {
                    '$lt': shop_offer_price
                }
            },
            {
                '$set': {
                    'max_price': shop_offer_price
                }
            }
        )
