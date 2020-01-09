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
            get_elements_from_mongo('shop_offers', request.GET['parameters'])
        else:
            get_elements_from_mongo('shop_offers')
        return response

    if request.method == 'POST':
        if 'item_id' not in request.POST:
            response.status_code = 400
            response.text = 'Не передан параметр item_id'
            return response
        shop_id = execute_sql(f"SELECT id FROM catalog_shop WHERE token = '{get_token_from_request(request)}';")[0]['id']
        offer_parameters = request.POST['parameters']
        offer_parameters['shop_id'] = shop_id
        offer_insert(offer_parameters)
        return response

@AccessDecorator(offer_parameters)
def offer(request):
    offer_id = request.matchdict['shop_offer_id']
    response = Response()

    if request.method == 'GET':
        shop_offer = get_elements_from_mongo('shop_offers', document_ids=[ObjectId(shop_offer_id)], only_one=True)
        response.text = shop_offer
        return response

    if request.method == 'PUT':
        parameters = request.json_body
        offer = get_elements_from_mongo('offer', document_ids=[offer_id], only_one=True)
        shop_id = offer['shop_id']
        token = get_token_from_request(request)
        if get_rights(token) != 3 and not execute_sql(f"SELECT 1 FROM catalog_shop WHERE id={shop_id} and token='{token}';"):
            response.status_code = 403
            return response
        offer_update_in_mongo(offer_id, parameters)
        return response

    if request.method == 'DELETE':
        offer_delete_from_elastic(offer_id)
