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
    data = es.search(index=index_name, scroll='2m', size=10000, body={})

    # Get the scroll ID and scroll size
    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])

    # create empty dataframe
    df = pd.DataFrame()

    # ignore FutureWarning
    warnings.simplefilter(action='ignore', category=FutureWarning)

    while scroll_size > 0:
        # retrieve the useful data from query
        output = [data['hits']['hits'][i]["_source"] for i in range(len(data["hits"]["hits"]))]

        # append data to the dataframe
        df = df.append(output, ignore_index=True)

        # scroll
        data = es.scroll(scroll_id=sid, scroll='2m')

        # Update the scroll ID
        sid = data['_scroll_id']

        # Get the number of results that returned in the last scroll
        scroll_size = len(data['hits']['hits'])

    df.to_pickle("pickles/" + index_name + ".p")



