from pyramid.response import Response
from authentification.access_control import *
from authentification.access_parameters import *
from authentification.decorators import AccessDecorator
from neo4j_utils.get import *
from neo4j_utils.add import *
from postgres_utils.utils import execute_sql
from redis_utils.cache import get_user_recommendation_from_cache, cache_user_recommendation
import psycopg2


@AccessDecorator(users_parameters)
def users(request):
    if request.method == 'GET':
        return Response(json=execute_sql('SELECT * FROM catalog_user;'))


@AccessDecorator(user_parameters)
def user(request):
    user_id = request.matchdict['user_id']
    response = Response()

    if request.method == 'GET':
        return Response(json=execute_sql(f'SELECT * FROM catalog_user WHERE id={user_id};')[0])

    if request.method == 'PUT':
        parameters = request.json_body
        query = f'UPDATE {appropriate_rights_names[parameters["access_type"]]} SET '
        del parameters['access_type']
        for key in parameters[:-1]:
            query += f"{key} = '{parameters[key]}',"
        query += f"{parameters[-1]} = {parameters[parameters[-1]]};"
        print(query)
        try:
            execute_sql(query, fetch=False)
        except psycopg2.Error as e:
            if e.pgcode == '42703':
                response.status_code = 400
                response.json = {'error_text': 'unknown parameter passed'}
                return response
            if e.pgcode == '42P10':
                response.status_code = 400
                response.json = {'error_text': 'data inconsistency'}
                return response
            else:
                return Response(e.pgerror)

    if request.method == 'DELETE':
        query = f'DELETE FROM catalog_user WHERE id = {user_id};'
        execute_sql(query)
        return response

    return Response()


@AccessDecorator(user_actions_parameters)
def user_actions(request):
    user_id = request.matchdict['user_id']
    if request.method == 'GET':
        token = get_token_from_request(request)
        if not has_rights('user', user_id, token):
            return Response(status=403)
        actions = get_user_actions(user_id, with_name=True)
        return Response(json=actions)

    if request.method == 'POST':
        if 'action_type' not in request.POST:
            return Response(status=400, json={'error_text': 'not action_type parameter'})
        if 'item_id' not in request.POST:
            return Response(status=400, json={'error_text': 'not item_id parameter'})
        action_type = request.POST['action_type'].lower()
        item_id = request.POST['item_id']
        add_user_action(user_id, action_type, item_id)
        return Response()


@AccessDecorator(recommended_items_parameters)
def user_recommended_items(request):
    user_id = request.matchdict['user_id']
    response = Response()
    if request.method == 'GET':
        token = get_token_from_request(request)
        if not has_rights('user', user_id, token):
            return Response(status=403)

        recommended_items = get_user_recommendation_from_cache(user_id)
        if not recommended_items:
            recommended_items = get_recommended_items_by_user_id(user_id, with_name=True)
            cache_user_recommendation(user_id, recommended_items)
        response.json = recommended_items
        response.content_type = 'application/json'
        return response
