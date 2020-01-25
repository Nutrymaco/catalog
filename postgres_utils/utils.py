import psycopg2
from settings import PG_HOST, PG_NAME

connection = psycopg2.connect(dbname=PG_NAME, host=PG_HOST, user='postgres')
connection.autocommit = True


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def execute_sql(query, fetch=True):
    cursor = connection.cursor()
    cursor.execute(query)
    if fetch:
        row = dictfetchall(cursor)
        return row


def process_sql_injection(query):
    return query


def get_query_for_insert(table_name, values, columns=None):
    query = f'INSERT INTO {table_name} {get_sql_columns_string(columns)} VALUES ({get_sql_values_string(values)});'
    return query


def get_sql_columns_string(columns):
    if not columns:
        return ''
    else:
        return str(columns).replace('[', '(').replace(']', ')').replace("'", "")


def get_sql_values_string(values):
    return str(values)[1:-1].replace('[', '(').replace(']', ')')


def get_query_for_select(table_name, fields=None, distinct=False, where=None, join=None):
    return f'SELECT {"DISTINCT" if distinct else ""} {get_sql_fields_string(fields)} FROM {table_name} ' \
        f'{" ".join(join) if join else ""} ' \
        f'{" ".join(where if where else "")};'


def get_query_for_delete(table_name, where=None):
    return f'DELETE FROM {table_name} ' \
        f'{" ".join(where if where else "")};'


def get_query_for_udate(table_name, where=None, set_list=None):
    return f'UPDATE {table_name} ' \
        f'{" ".join(set_list) if set_list else ""}' \
        f'{" ".join(where if where else "")};'


def get_sql_fields_string(fields):
    if not fields or fields == '*':
        return '*'
    return str(fields)[1:-1].replace("'", "")


def get_join(original_table, join_table, orig_obj, join_obj):
    return f'JOIN {join_table} ON {original_table}.{orig_obj} = {join_table}.{join_obj}'


def get_where(obj1, obj2, equal=True):
    return f'WHERE {obj1} {"=" if equal else "!="} {obj2}'


def get_set(obj1, obj2):
    return f'SET {obj1} = {obj2}'
