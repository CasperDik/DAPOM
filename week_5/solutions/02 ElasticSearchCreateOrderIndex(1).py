# Dapom Week 5 Practical B
# Wout van Wezel, 2020
from datetime import datetime
from elasticsearch import Elasticsearch
import json
es = Elasticsearch([{'host':'127.0.0.1', 'port':9200}])
es.indices.create(index='products', ignore=400)
es.index(index="products", body={"type": "trousers", "region":"france", "price": 10})
es.index(index="products", body={"type": "jacket", "region":"spain", "price": 25})
es.index(index="products", body={"type": "socks", "region":"france", "price": 5})
es.index(index="products", body={"type": "trousers", "region":"france", "price": 5})
es.index(index="products", body={"type": "socks", "region":"spain", "price": 7})
print("Records added")
