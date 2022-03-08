from elasticsearch import Elasticsearch

def query_locations(password_elasticsearch):
    """query all location from elasticsearch"""
    pass

    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # todo: query
    # todo: extract right list
    # todo: return list with locations


def query_forecasts(password_elasticsearch):
    """"query all forecast from elasticsearch"""
    pass

    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # todo: query
    # todo: extract right list
    # todo: return list with forecast

