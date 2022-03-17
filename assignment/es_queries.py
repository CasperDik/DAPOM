from elasticsearch import Elasticsearch
import pandas as pd
import warnings
import pickle

def query_all_entries(password_elasticsearch, index_name):
    """query all location from elasticsearch index: assignment_geo_coords"""

    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # todo: exactly learn how this scrolling works --> for oral exam
    # Init scroll by search
    data = es.search(index=index_name, scroll="2m", size=10000, body={})

    # Get the scroll ID and scroll size
    sid = data["_scroll_id"]
    scroll_size = len(data["hits"]["hits"])

    # create empty dataframe
    df = pd.DataFrame()

    # ignore FutureWarning
    warnings.simplefilter(action="ignore", category=FutureWarning)

    while scroll_size > 0:
        # retrieve the useful data from query
        output = [data["hits"]["hits"][i]["_source"] for i in range(len(data["hits"]["hits"]))]

        # append data to the dataframe
        df = df.append(output, ignore_index=True)

        # scroll
        data = es.scroll(scroll_id=sid, scroll="2m")

        # Update the scroll ID
        sid = data["_scroll_id"]

        # Get the number of results that returned in the last scroll
        scroll_size = len(data["hits"]["hits"])

    df.to_pickle("pickles/" + index_name + ".p")


def query_count_locations(password_elasticsearch: str, list_to_exclude: list):
    """add sth.."""
    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # search body of a query to get value counts of each postcode while excluding holidays
    search_body = {"query": {
            "bool": {
                "must_not": list_to_exclude
            }
        },
        "size": 0,
        "aggs": {
            "count": {
                "terms": {
                    "field": "postcode.keyword", "size": 10000
                }
            }
        }
    }
    # run the query
    data = es.search(index="assignment_forecasts23", body=search_body)

    # extract and return the relevant data
    return data["aggregations"]["count"]["buckets"]


def query_count_district(password_elasticsearch: str, list_to_exclude: list):
    """add sth.."""
    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # search body of a query to get the counts per districts while excluding holidays
    search_body = {"query": {
        "bool": {
            "must_not": list_to_exclude
        }
    },
        "size": 0,
        "aggs": {
            "count": {
                "terms": {
                    "size": 100,
                    "script": {
                        "inline": "doc['postcode.keyword'].getValue().substring(0,4)"
                    }   # to get from location to district. Takes first 4 elements of string e.g. 9711RS --> 9711
                }
            }
        }
    }

    # run the query
    data = es.search(index="assignment_forecasts23", body=search_body)

    # extract and return the relevant data
    return data["aggregations"]["count"]["buckets"]
