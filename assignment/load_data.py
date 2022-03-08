from elasticsearch import Elasticsearch
import time
from loader import ingest_csv_file_into_elastic_index


def load_to_es(elastic_client: Elasticsearch, filename: str, index_name: str, buffer_size=None, mapping=None):
    """
    Creates a new index in Elasticsearch and uploads the data of a .csv to it. Mapping can be specified but is not
    required.
    """
    tic = time.time()

    # create new index in elasticsearch
    elastic_client.indices.create(index=index_name, ignore=400, mappings=mapping)

    # load csv in index using loader.py
    ingest_csv_file_into_elastic_index(csv_file_name=filename, elastic_client=elastic_client, index_name=index_name,
                                       buffer_size=buffer_size)

    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of loading ', index_name, ': {:.2f} seconds'.format(elapsed_time))


def load_data(password_elasticsearch):
    """
    Connects to Elasticsearch and loads the data of the 3 .csv files using the function "load_to_es". Requires your
    elasticsearch password as input.
    """
    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # todo: can adjust mapping if needed
    # http://localhost:9200/assignment_geo_coords/_mapping?pretty
    # es.indices.put_mapping(index="", body={})

    # load geo coords
    load_to_es(es, filename="input_data/geo_coordinates_per_each_location.csv", index_name="assignment_geo_coords",
               buffer_size=5000)

    # load forecasts
    load_to_es(es, filename="input_data/forecasts_2023.csv", index_name="assignment_forecasts23", buffer_size=15000)

    # load distances
    load_to_es(es, filename="input_data/distances_between_locations.csv", index_name="assignment_distances",
               buffer_size=150000)


