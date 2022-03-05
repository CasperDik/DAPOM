from elasticsearch import Elasticsearch
import json

# tell python were ES can be found
password = "."
es = Elasticsearch(hosts="http://elastic:" + password + "@localhost:9200")
# es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200, 'scheme': 'http'}])

# result = es.get(index="persons", id=2)
# print(result)
# print(result['_source']['timestamp'])

search_body = {
 'size': 100,
 'query': {
 'bool': {
 'must': {
 'term':{
 'hobby': "netflix"
 }
 }
 }
 }
}
result = dict(es.search(index="persons", body=search_body))

print(json.dumps(result, indent=4))

print([result["hits"]["hits"][i]["_source"] for i in range(len(result["hits"]["hits"]))])
print([result["hits"]["hits"][i]["_source"]["name"] for i in range(len(result["hits"]["hits"]))])
