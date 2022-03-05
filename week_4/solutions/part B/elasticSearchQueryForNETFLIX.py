# Dapom Week 4 Practical B, example 5.4
# Wout van Wezel, 2020

from elasticsearch import Elasticsearch
import json

es =Elasticsearch([{'host':'127.0.0.1', 'port': 9200}])
# you define a dictionary like data structure
# which is the body of the query question
search_body = {
    'query': {
        'bool':{
            'must':{
                'term':{
                    'hobby': 'netflix'
                }
            }
        }
    }
}
# make sure that the index persons is still on the
# local server, check by looking at http://localhost:9200/persons
result =es.search(index="persons", body=search_body)
#print (result) # this is ugly
print(json.dumps(result, indent=4))

print("exit code 0")
