from pyramid.response import Response
from authentification.decorators import AccessDecorator
from authentification.access_parameters import *
from mongo_utils.get import *
from mongo_utils.insert import *
from mongo_utils.delete import *
from mongo_utils.update import *
from elastic_utils.search import *
from elastic_utils.index import *
from elastic_utils.delete import *
from elasticsearch.exceptions import NotFoundError
import json
from pprint import pprint


@AccessDecorator(items_access_parameters)
def items(request):
    response = Response()
    response.content_type = 'text/json'
    print('in items')
    if request.method == 'GET':  # выборка
        parameters = request.GET['parameters']
        parameters = json.loads(parameters)
        text = request.GET['text']
        if text:
            id_list = search_items_from_elastic(text, only_id=True)
            if not id_list:
                response.text = '[]'
                return response
            items_to_response = get_elements_from_mongo('items', parameters, id_list)
        else:
            items_to_response = get_elements_from_mongo('items', parameters)
        response.status_code = 200
        response.text = str(items_to_response)
        return response

    elif request.method == 'POST':
        parameters = json.loads(request.POST['parameters'])
        mongo_flag = False
        try:
            item_id = item_insert(parameters)
            mongo_flag = True
        except:
            pass
        if mongo_flag:
            try:
                item_index({
                    'name': parameters['name'],
                    'description': parameters['description']
                }, item_id=str(item_id))
            except:
                item_delete_from_mongo(item_id)
        return response

    return Response('123')


@AccessDecorator(item_access_parameters)
def item(request):
    response = Response()
    item_id = request.matchdict['item_id']
    if request.method == 'GET':
        item_to_response = get_elements_from_mongo('items', document_ids=[item_id])
        response.status_code = 200
        return Response(str(item_to_response))
    elif request.method == 'PUT':
        item_id = request.matchdict['item_id']
        item_parameters = request.json_body
        print(item_parameters)
        print(item_id)
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



