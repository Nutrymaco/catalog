from pyramid.response import Response
from authentification.access_control import *

def users(request):
    ...


def user(request):
    user_id = request.matchdict['user_id']
    print(request.__dir__())
    print(list(request.headers))
    print(request.authorization.params)  # first - auth_type
    return Response()


def user_token(request):
    response = Response()
    user_id = request.matchdict['user_id']
    if not user_exists(user_id, 1):
        response.status_code = 404
        return response
    if request.method == "GET":  # get
        if 'login' not in request.GET or 'password' not in request.GET:
            response.status_code = 401
            return response
        login = request.GET['login']
        password = request.GET['password']
        token = get_token(login, password, 1)
        if token:
            return Response(token)
        else:
            response.status_code = 401
            return response

    if request.method == 'PUT':  # refresh
        if 'login' not in request.GET or 'password' not in request.GET:
            response.status_code = 401
            return response
        login = request.GET['login']
        password = request.GET['password']

        if not user_exists(user_id, 1):
            response.status_code = 401
            return response

        token = refresh_and_get_token(login, password, 2)
        return Response(token)
