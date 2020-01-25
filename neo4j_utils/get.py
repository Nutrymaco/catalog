from neo4j_utils.graph import GraphDriver
from mongo_utils.get import get_elements_from_mongo
from neo4j_utils.graph import g


def get_user_actions(user_id, with_name=False):
    query_for_look = f'''
        MATCH (User{{user_id: {user_id}}})-[:LOOK]->(item:Item)
        RETURN item
    '''
    query_for_buy = f'''
        MATCH (User{{user_id: {user_id}}})-[:BUY]->(item:Item)
        RETURN item
    '''

    looked_item_id_list = [i.value()['item_id'] for i in g.run_query(query_for_look)]
    bought_item_id_list = [i.value()['item_id'] for i in g.run_query(query_for_buy)]

    looked_item_id_list = reduce_array(looked_item_id_list)
    bought_item_id_list = reduce_array(bought_item_id_list)

    if with_name:
        looked_item_id_list = name_enrichment(looked_item_id_list)
        bought_item_id_list = name_enrichment(bought_item_id_list)

    return {
        'look': looked_item_id_list,
        'buy': bought_item_id_list
    }


def get_recommended_items_by_user_id(user_id, with_name=False):
    query = f'''
        MATCH (subj:User{{user_id:{user_id}}})-[:LOOK|BUY]->(common_item:Item)<-[:LOOK|BUY]-(person:User),
        (person)-[:BUY]->(bought_item:Item)
        WHERE subj <> person and bought_item <> common_item
        RETURN person.user_id AS id, COUNT(distinct common_item) AS common_item_count, COLLECT( distinct bought_item) as
        recommended_items
        ORDER BY common_item_count DESC
    '''

    item_collections = g.run_query(query)
    recommended_item_id_list = []
    for collection in item_collections:
        for item in collection['recommended_items']:
            recommended_item_id_list.append(item['item_id'])

    recommended_item_id_list = reduce_array(recommended_item_id_list)
    recommended_items = []
    for item_id in recommended_item_id_list:
        if with_name:
            item = get_elements_from_mongo('items', document_ids=[item_id], only_one=True)
            recommended_items.append({
                'item_id': item_id,
                'name': item['name'] if item else ''
                }
            )
        else:
            recommended_items.append({'item_id': item_id})

    return {
        'recommendations': recommended_items
    }


def get_similar_items(item_id, with_name=False):
    query = f'''
        MATCH (subj:User)-[:LOOK|BUY]->(i:Item{{item_id:"{item_id}"}}),
        (subj:User)-[:LOOK|BUY]->(similar_item:Item)
        WHERE similar_item <> i
        RETURN similar_item.item_id as item_id
    '''
    similar_items = g.run_query(query)
    item_id_list = reduce_array([i['item_id'] for i in similar_items])
    items = []
    for item_id in item_id_list:
        if with_name:
            item = get_elements_from_mongo('items', document_ids=[item_id], only_one=True)
            items.append({
                'item_id': item_id,
                'name': item['name'] if item else ''
            })
        else:
            items.append({
                'item_id': item_id
            })
    return {
        'items': items
    }


# [1, 2, 4, 1, 4, 4] -> [4, 1, 2]
def reduce_array(array):
    dict_count = {num: array.count(num) for num in array}
    return [num for num in sorted(dict_count, key=lambda num: dict_count[num], reverse=True)]


def name_enrichment(id_list):
    enriched_list = list()
    for id in id_list:
        doc = get_elements_from_mongo('items', document_ids=[id], only_one=True)
        enriched_list.append({
            'id': id,
            'name': doc['name'] if doc else ''
        })
    return enriched_list



if __name__ == "__main__":
    #print(reduce_array([1, 2, 4, 1, 4, 4]))

    print(get_similar_items("5e178d5bef34d4212f79f90e"))
    print(get_recommended_items_by_user_id(5))