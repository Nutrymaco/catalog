from postgres_utils.utils import execute_sql
from random import randint
appropriate_roles = {
    1: 'catalog_user',
    2: 'catalog_shop',
    3: 'catalog_worker'
}

appropriate_rights_names = {
    'user': 'catalog_user',
    'shop': 'catalog_shop',
    'worker': 'catalog_worker'
}


def get_token_from_request(request):
    if 'Authorization' in list(request.headers):
        return dict(request.headers)['Authorization']
    else:
        return None


def get_rights(token) -> int:
    for key in appropriate_roles:
        if execute_sql(f"SELECT 1 FROM {appropriate_roles[key]} WHERE access_token='{token}'"):
            return key
    return -1


'''
def get_token(login, password, level):
    token = execute_sql(f'SELECT token FROM {appropriate_roles[level]} WHERE login = "{login}" and password = "{password}"')
    if token:
        return token
    else:
        return None
'''


def has_rights(rights_name, id, token):
    return execute_sql(f"SELECT 1 FROM {appropriate_rights_names[rights_name]} WHERE id={id} and access_token='{token}';")


def user_exists(id, level):
    if execute_sql(f'SELECT 1 FROM {appropriate_roles[level]} WHERE id={id}'):
        return True
    return False


if __name__ == '__main__':
    print(has_rights('user', 5, 'myhszeqzlwidduix'))