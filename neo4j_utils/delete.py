from neo4j_utils.graph import GraphDriver
from neo4j_utils.graph_utils import get_string_params_from_dict
from neo4j_utils.graph import g


def delete_node(node_type, parameters=None, force=True):
    if force:
        query = f'''
            MATCH ()-[r]->({node_type}{get_string_params_from_dict(parameters)})
            DELETE r
        '''
        g.run_query(query)
        query = f'''
            MATCH ({node_type}{get_string_params_from_dict(parameters)})-[r]->()
            DELETE r
        '''
        g.run_query(query)

    query = f'''
        MATCH (n:{node_type}{get_string_params_from_dict(parameters)})
        DELETE n
    '''
    g.run_query(query)


def delete_user_node(user_id):
    delete_node('User', {'user_id': user_id})


def delete_item_node(item_id):
    delete_node('Item', {'item_id': item_id})


if __name__ == "__main__":
    from neo4j_utils.add import add_user_action
    # delete_node('User', {'user_id': 5})
    delete_node('Item')