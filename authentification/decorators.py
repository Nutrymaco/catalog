from .access_control import *
from pyramid.response import Response


class AccessDecorator:
    def __init__(self, access_parameters):
        self.access_parameters = access_parameters

    def __call__(self, view):
        def check_access(request):
            response = Response()

            if request.method not in self.access_parameters['methods']:
                response.status_code = 405
                return response

            need_rights = self.access_parameters['methods'][request.method]
            if need_rights == 0:
                return view(request)

            token = get_token_from_request(request)
            if not token:
                response.status_code = 401
                return response

            rights = get_rights(token)

            if rights not in need_rights:
                response.status_code = 403
                return response

            return view(request)
        return check_access
