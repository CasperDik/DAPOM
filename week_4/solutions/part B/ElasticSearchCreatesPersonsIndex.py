# Dapom Week 4 Practical B, example 5.3
# Wout van Wezel, 2020

from datetime import datetime
from elasticsearch import Elasticsearch
import json

# create an ES data manager object, that is, es
es = Elasticsearch([{'host':'127.0.0.1', 'port':9200}])

# create a database (or "index" in ES-speak) for persons
es.indices.create(index='persons', ignore=400)

# add a person
es.index(index="persons",
    id=1,
    body={"name": "wout",
    "hobby":"programming",
    "age": 49,
    "timestamp":datetime.now()
    }
)
# add another person
es.index(index="persons",
    id=2,
    body={"name":"anna",
    "hobby": "netflix",
    "age": 16,
    "timestamp": datetime.now()
    }
)
# query the database, by using the get method
result = es.get(index="persons", id=1)
# print the query result
print(json.dumps(result, indent=4))
# print a part of the query result, using the dictionary indexing style
# because the result is indeed a dictionary
print(result['_source']['timestamp'])
# you may delete the database
#es.indices.delete(index='persons', ignore=[400, 404])
# but don't because you want the next Python script to query it again...

print("exit code 0")
