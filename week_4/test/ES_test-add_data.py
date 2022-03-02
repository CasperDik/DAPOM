from elasticsearch import Elasticsearch
from datetime import datetime

# tell python were ES can be found
es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200, 'scheme': 'http'}])

# create a table and ignore 400 error(table already exists)
es.indices.create(index='persons', ignore=400)

es.index(index="persons",
         id=1,
         body={"name": "wout",
               "hobby":  "netflix",
               "age": 49,
                "timestamp": datetime.now()
               }
         )

es.index(index="persons",
         id=2,
         body={"name": "anna",
               "hobby": "netflix",
               "age": 16,
               "timestamp": datetime.now()
               }
         )

result = es.get(index="persons", id=2)

# es.indices.delete(index='persons', ignore=[400, 404])