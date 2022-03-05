# Dapom Week 4 Practical B Assignment, create taxi index
# Wout van Wezel, 2020

from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost', 'port': 9200}])
# create a record pattern, imposing the types we want
# for datetime and geolocation points
settings = {
    'settings': {
        "number_of_shards" : 3
                },
        'mappings': {
            'properties': {
                'pickup_datetime': {'type': 'date', "format": "yyyy-MM-dd HH:mm:ss" },
                    'dropoff_datetime': {'type': 'date', "format": "yyyy-MM-dd HH:mm:ss" },
                        'pickup_location': {'type': 'geo_point' },
                            'dropoff_location': {'type': 'geo_point'}
                           }
                    }
            }
# this will create an empty index, but with a data type pattern for
# certain fields we want to use later, and we cannot "take" them as strings
es.indices.create(index='taxi', body=settings)
# here, the use of the error avoidance via ignore = 400 is not recommended
# because it will destroy the index already created if we run this code
# after we used elasticsearch_loader to put the index in the memory and
# we will have to do it again if it is destroyed
print("index 'taxi' created")

print("exit code 0")
