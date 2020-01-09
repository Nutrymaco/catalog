from pyramid.response import Response
from authentification.decorators import AccessDecorator
from authentification.access_parameters import shop_offers_parameters, shop_offer_parameters
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


def shops(request):
    ...


def shop(request):
    ...

