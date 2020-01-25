from neo4j import GraphDatabase
from .graph_utils import get_query_for_create_node, get_query_for_match_node, get_query_for_creating_couple, \
    get_query_for_check_edge, get_query_for_match_node_in_couple


class GraphNode:
    def __init__(self, type='', **params):
        self.type = type
        self.params = params


class GraphEdge:
    def __init__(self, type='', **params):
        self.type = type
        self.params = params


class GraphDriver:
    def __init__(self, uri=f'bolt://127.0.0.1', user='neo4j', password='test'):
        self._driver = GraphDatabase.driver(uri=uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_node_if_not_exists(self, node):
        with self._driver.session() as session:
            exists = session.write_transaction(self._node_exists, node)
            if not exists:
                session.write_transaction(self._create_node_if_not_exist, node)

    def create_couple_if_not_exists(self, node1, edge, node2):
        self.create_node_if_not_exists(node1)
        self.create_node_if_not_exists(node2)
        with self._driver.session() as session:
            if not session.write_transaction(self._couple_exists, node1, edge, node2):
                session.write_transaction(self._create_couple, node1, edge, node2)

    def get_start_node_list(self, edge, end_node, start_node=GraphNode()):
        with self._driver.session() as session:
            node_list = session.write_transaction(self._get_node_list_in_couple, start_node, edge, end_node)
        return node_list

    def get_end_node_list(self, start_node, edge, end_node=GraphNode()):
        with self._driver.session() as session:
            node_list = session.write_transaction(self._get_node_list_in_couple, start_node, edge, end_node, revert=True)
        return node_list

    def run_query(self, query):
        with self._driver.session() as session:
            result = session.write_transaction(self._run_query, query)
        return result

    def get_edge_list(self, start_node, end_node, edge=GraphEdge()):
        ...

    @staticmethod
    def _create_couple(tx, node1, edge, node2):
        # print(get_query_for_creating_couple(node1, edge, node2, couple_type))
        tx.run(get_query_for_creating_couple(node1, edge, node2))

    @staticmethod
    def _create_node_if_not_exist(tx, node):
        # print(get_query_for_create_node(node.type, **node.params))
        tx.run(get_query_for_create_node(node))

    @staticmethod
    def _node_exists(tx, node):
        # print(get_query_for_match_node(node.type, **node.params))
        node = tx.run(get_query_for_match_node(node))
        return bool(node.single())

    @staticmethod
    def _couple_exists(tx, node1, edge, node2):
        couple = tx.run(get_query_for_check_edge(node1, edge, node2))
        return bool(couple.single())

    @staticmethod
    def _get_node_list_in_couple(tx, match_node, edge, other_node, **kwargs):
        node_list = tx.run(get_query_for_match_node_in_couple(match_node, edge, other_node, **kwargs))
        return node_list.records()

    @staticmethod
    def _run_query(tx, query):
        result = tx.run(query)
        return result.records()


g = GraphDriver()


def test():
    i = GraphNode('NOUN', text='i')
    go = GraphEdge('ACT_ON', text='go')
    home = GraphNode('NOUN', text='home')
    g.create_couple_if_not_exists(i, go, home)
    values = g.get_end_node_list(i, go)

    for val in values:
        print(val.value().get('text'))

    values = g.get_start_node_list(go, home)
    for val in values:
        print(val.value().get('text'))


def test_write():
    ...
