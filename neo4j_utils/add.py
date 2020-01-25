from neo4j_utils.graph import GraphDriver
from neo4j_utils.graph import g


def add_user_action(user_id, action_type, item_id):
    query = f'''
        MERGE (u:User{{user_id: {user_id}}})
        MERGE (i:Item{{item_id: "{item_id}"}})
        MERGE (u)-[:{action_type.upper()}]->(i)
    '''
    g.run_query(query)
