from postgres_utils.utils import execute_sql
from random import randint
appropriate_roles = {
    1: 'catalog_user',
    2: 'catalog_shop',
    3: 'catalog_stuff'
}


def get_token_from_request(request):
    if 'Authorization' in list(request.headers):
        return dict(request.headers)['Authorization']
    else:
        return None


def get_rights(token) -> int:
    for key in appropriate_roles:
        if execute_sql(f"SELECT 1 FROM {appropriate_roles[key]} WHERE token='{token}'"):
            return key
    return -1


def get_token(login, password, level):
    token = execute_sql(f'SELECT token FROM {appropriate_roles[level]} WHERE login = "{login}" and password = "{password}"')
    if token:
        return token
    else:
        return None


def refresh_and_get_token(login, password, level):
    token = ''
    for _ in range(128):
        token += chr(randint(0, 64))
    execute_sql(f'UPDATE {appropriate_roles[level]} SET token = "{token}" WHERE'
                f'login = "{login}" and password = "{password}"', fetch=False)
    return token


def user_exists(id, level):
    if execute_sql(f'SELECT 1 FROM {appropriate_roles[level]} WHERE id={id}'):
        return True
    return False
