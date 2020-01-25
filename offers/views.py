from pyramid.response import Response
from authentification.decorators import AccessDecorator
from authentification.access_parameters import *
from authentification.access_control import *
from mongo_utils.get import *
from mongo_utils.insert import *
from mongo_utils.delete import *
from mongo_utils.update import *
from elastic_utils.search import *
from elastic_utils.index import *
from elastic_utils.delete import *
from elasticsearch.exceptions import NotFoundError
from postgres_utils.utils import execute_sql
import json


@AccessDecorator(offers_parameters)
def offers(request):
    response = Response()

    if request.method == 'GET':
        if 'parameters' in request.GET:
            offer_list = get_elements_from_mongo('offers', request.GET['parameters'])
        else:
            offer_list = get_elements_from_mongo('offers')
        for offer in offer_list:
            offer['item_id'] = str(offer['item_id'])
        return Response(json=offer_list)

    if request.method == 'POST':
        if type(request.POST['parameters']) == str:
            parameters = json.loads(request.POST['parameters'])
        else:
            parameters = request.POST['parameters']

        if 'item_id' not in parameters:
            response.status_code = 400
            response.json = {'error_text': 'item_id parameter not passed'}
            return response
        if 'price' not in parameters:
            response.status_code = 400
            response.json = {'error_text': 'price parameter not passed'}
            return response

        shop_id = execute_sql(f"SELECT id FROM catalog_shop WHERE access_token = '{get_token_from_request(request)}';")[0]['id']

        parameters['shop_id'] = shop_id
        offer_insert(parameters)
        return response


@AccessDecorator(offer_parameters)
def offer(request):
    offer_id = request.matchdict['shop_offer_id']
    response = Response()

    if request.method == 'GET':
        shop_offer = get_elements_from_mongo('offers', document_ids=[ObjectId(offer_id)], only_one=True)
        response.json = shop_offer
        response.content_type = 'application/json'
        return response

    if request.method == 'PUT':
        parameters = request.json_body
        offer = get_elements_from_mongo('offers', document_ids=[offer_id], only_one=True)
        shop_id = offer['shop_id']
        token = get_token_from_request(request)
        if get_rights(token) != 3 and not has_rights('shop', shop_id, token):
            response.status_code = 403
            return response
        offer_update_in_mongo(offer_id, parameters)
        return response

    if request.method == 'DELETE':
        offer_delete_from_mongo(offer_id)
        return Response()
