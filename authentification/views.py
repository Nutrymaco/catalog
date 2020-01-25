from pyramid.response import Response
from authentification.access_control import *
from authentification.access_parameters import *
from authentification.decorators import AccessDecorator
from postgres_utils.utils import get_query_for_insert
import psycopg2
from psycopg2.errorcodes import UNDEFINED_COLUMN
from random import randint


def register(request):
    parameters = {}
    response = Response()
    if request.method == 'GET':
        parameters = request.GET
    if request.method == 'POST':
        parameters = request.POST

    if 'access_type' not in parameters:
        response.status_code = 400
        response.text = 'не передан параметр access_type'

    access_token = generate_token()
    refresh_token = generate_token()

    table_name = appropriate_rights_names[parameters["access_type"]]
    del parameters['access_type']

    query = get_query_for_insert(table_name, list(parameters.values()) + [access_token, refresh_token],
                                 list(parameters.keys()) + ['access_token', 'refresh_token'])
    try:
        execute_sql(query, fetch=False)
    except psycopg2.Error as e:
        if e.pgcode == '42703':
            response.status_code = 400
            response.json = {'error_text': 'unknown parameter passed'}
            return response
        if e.pgcode == '23503':
            response.status_code = 400
            response.json = {'error_text': 'data inconsistency'}
            return response
        else:
            return Response(e.pgerror)

    return Response(json={'access_token': access_token, 'refresh_token': refresh_token})


def refresh(request):
    if request.method == 'GET':
        ...
    if request.method == 'POST':
        ...


def generate_token():
    token = ''
    for _ in range(16):
        token += chr(randint(100, 122))
    return token
