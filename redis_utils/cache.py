import json
import redis
from settings import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def cache_user_recommendation(user_id, recommended_items, sec=24*3600):
    r.set(f'user:{user_id}', json.dumps(recommended_items), ex=sec)


def get_user_recommendation_from_cache(user_id):
    recommended_items = r.get(f'user:{user_id}')
    return json.loads(recommended_items) if recommended_items else None


def cache_item_similar_items(item_id, similar_items, sec=24*3600):
    r.set(f'item:{item_id}', json.dumps(similar_items), ex=sec)


def get_item_similar_items_from_cache(item_id):
    similar_items = r.get(f'item:{item_id}')
    return json.loads(similar_items) if similar_items else None


if __name__ == "__main__":
    #cache_item_similar_items(5, [{"1":12}, 2, 4])
    print(get_item_similar_items_from_cache(5))