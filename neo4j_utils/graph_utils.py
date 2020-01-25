def get_query_for_create_node(node, node_name='node'):
    return f'CREATE ({node_name}:{node.type}{get_string_params_from_dict(node.params)})'


def get_query_for_match_node(node, node_name='node', return_result=True):
    query = f'MATCH ({node_name}'
    if node.type:
        query += f': {node.type}'
    query += ')'
    if node.params:
        query += '\nWHERE'
        for key in list(node.params)[:-1]:
            query += f' {node_name}.{str(key)} = "{node.params[key]}" AND'
        last_key = list(node.params)[-1]
        query += f' {node_name}.{last_key} = "{node.params[last_key]}"'
        if return_result:
            query += f'\nreturn {node_name}'
    return query


def get_query_for_creating_couple(node1, edge, node2):
    query = get_query_for_match_node(node1, node_name='node1', return_result=False) + ' \n'
    query += get_query_for_match_node(node2, node_name='node2', return_result=False) + ' \n'
    query += f'CREATE (node1)-[:{edge.type}{get_string_params_from_dict(edge.params)}]->(node2)'
    return query


def get_query_for_merging_couple(node1, edge, node2):
    query = get_query_for_match_node(node1, node_name='node1', return_result=False) + ' \n'
    query += get_query_for_match_node(node2, node_name='node2', return_result=False) + ' \n'
    query += f'MERGE (node1)-[:{edge.type}{get_string_params_from_dict(edge.params)}]->(node2)'
    return query


def get_query_for_check_edge(node1, edge, node2):
    query = get_query_for_match_node(node1, node_name='node1', return_result=False) + '\n'
    query += get_query_for_match_node(node2, node_name='node2', return_result=False) + '\n'
    query += f'MATCH (node1)-[:{edge.type}{get_string_params_from_dict(edge.params)}]->(node2)\n'
    query += 'RETURN node1, node2'
    return query


def get_string_params_from_dict(params: dict) -> str:
    string_params = '{'
    if params:
        for key in list(params)[:-1]:
            par = f'"{params[key]}"' if type(params[key]) == str else f'{str(params[key])}'
            string_params += str(key) + f': {par},'
        last_key = list(params)[-1]
        par = f'"{params[last_key]}"' if type(params[last_key]) == str else f'{str(params[last_key])}'
        string_params += str(last_key) + f':{par}'
    string_params += '}'
    return string_params


def get_query_for_match_node_in_couple(match_node, edge, other_node, revert=False):
    match_node_name = 'node1'
    other_node_name = 'node2'
    query = get_query_for_match_node(match_node, node_name=match_node_name, return_result=False) + '\n'
    query += get_query_for_match_node(other_node, node_name=other_node_name, return_result=False) + '\n'
    if revert:
        match_node_name, other_node_name = other_node_name, match_node_name

    query += f'MATCH (node1)-[:{edge.type}{get_string_params_from_dict(edge.params)}]->(node2)\n'
    query += f'RETURN {match_node_name}'

    return query
