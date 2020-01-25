from pyramid.response import Response
from authentification.decorators import AccessDecorator
from authentification.access_parameters import *
from authentification.access_control import get_token_from_request
from mongo_utils.get import *
from mongo_utils.insert import *
from mongo_utils.delete import *
from mongo_utils.update import *
from elastic_utils.search import *
from elastic_utils.index import *
from elastic_utils.delete import *
from neo4j_utils.get import *
from elasticsearch.exceptions import NotFoundError
from redis_utils.cache import get_item_similar_items_from_cache, cache_item_similar_items
from postgres_utils.utils import execute_sql
import json
from pprint import pprint


@AccessDecorator(items_access_parameters)
def items(request):
    response = Response()
    response.content_type = 'text/json'
    if request.method == 'GET':  # выборка
        if 'parameters' in request.GET:
            parameters = request.GET['parameters']
            parameters = json.loads(parameters)
        else:
            parameters = {}

        if 'text' in request.GET:
            text = request.GET['text']
        else:
            text = ''

        if text:
            id_list = search_items_from_elastic(text, only_id=True)
            if not id_list:
                response.text = '[]'
                return response
            items_to_response = get_elements_from_mongo('items', parameters, id_list)
        else:
            items_to_response = get_elements_from_mongo('items', parameters)
        response.status_code = 200
        response.json = items_to_response
        return response

    elif request.method == 'POST':
        parameters = json.loads(request.POST['parameters'])
        mongo_flag = False
        token = get_token_from_request(request)
        result = execute_sql(f"SELECT id from catalog_shop WHERE access_token='{token}';")
        if result:
            parameters['shop_id'] = result[0]['id']
        try:
            item_id = item_insert(parameters)
            mongo_flag = True
        except Exception as e:
            print(e)
        if mongo_flag:
            try:
                item_index(parameters={
                    'name': parameters['name'],
                    'description': parameters['description']
                }, item_id=str(item_id))
            except Exception as e:
                print(e)
                item_delete_from_mongo(item_id)
        return response


@AccessDecorator(item_access_parameters)
def item(request):
    response = Response()
    item_id = request.matchdict['item_id']
    if request.method == 'GET':
        item_to_response = get_elements_from_mongo('items', document_ids=[item_id], only_one=True)
        response.status_code = 200
        response.json = item_to_response
        response.content_type = 'application/json'
        return response
    elif request.method == 'PUT':
        item_id = request.matchdict['item_id']
        item_parameters = request.json_body
        item_update_in_mongo(item_id, item_parameters)
        item_index(item_id, item_parameters)
        pprint(item_parameters)
        return response
    elif request.method == 'DELETE':
        item_id = request.matchdict['item_id']
        item_delete_from_mongo(item_id)
        try:
            item_delete_from_elastic(item_id)
        except NotFoundError:
            pass
        return response


@AccessDecorator(similar_items_parameters)
def item_similar_items(request):
    item_id = request.matchdict['item_id']
    response = Response()
    if request.method == 'GET':
        similar_items = get_item_similar_items_from_cache(item_id)
        if not similar_items:
            similar_items = get_similar_items(item_id, with_name=True)
            cache_item_similar_items(item_id, similar_items)
        response.json = similar_items
        response.content_type = 'application/json'
        return response
