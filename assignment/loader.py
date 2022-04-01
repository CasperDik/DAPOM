from elasticsearch import Elasticsearch, helpers
import pandas as pd
import uuid
import time
import orjson


def ingest_csv_file_into_elastic_index(csv_file_name, elastic_client: Elasticsearch, index_name, buffer_size=5000):
    tic = time.time()

    data = pd.read_csv(csv_file_name, engine="c", chunksize=buffer_size)
    i = 0
    for chunk in data:
        json_list = orjson.loads(chunk.to_json(orient='records'))
        try:
            response = helpers.bulk(elastic_client, bulk_json(json_buffer=json_list, _index=index_name))
            i += 1
            print("bulk_json() RESPONSE for chunk:", i, response)
        except Exception as e:
            print("\nERROR:", e)

    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of loading ', index_name, ': {:.2f} seconds'.format(elapsed_time))

def bulk_json(json_buffer, _index):
    for doc in json_buffer:
        # use a `yield` generator so that the data
        # isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_id": uuid.uuid4(),
                "_source": doc
            }