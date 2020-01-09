from neo4j_utils.graph import GraphDriver

g = GraphDriver()


def get_recommendations_by_user_id(user_id):
    query = f'''
        MATCH (subj:User{{user_id:{user_id}}})
        MATCH (subj)-[:WATCH|BUY]->(common_item:Item)<-[:WATCH|BUY]-(person:User)
        MATCH (person)-[:BUY]->(bought_item:Item)
        RETURN person.name AS name, COUNT(distinct common_item) AS item_count, COLLECT( distinct buyed_item)
        ORDER BY item_count DESC
    '''
    items = g.run_query(query)
    return items


def get_recommendations_by_items(items):
    query = f'''
        MATCH (person:USER)-[:WATCH|BUY]->(common_item:Item)
        MATCH (person)-[:BUY]->(bought_item:Item)
        RETURN person.name AS name, COUNT(distinct common_item) AS item_count, COLLECT( distinct buyed_item)
        ORDER BY item_count DESC
    '''
