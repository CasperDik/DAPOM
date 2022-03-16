# Dapom Week 5 Practical B Assignment
# Wout van Wezel, 2020
from elasticsearch import Elasticsearch
import json

es =Elasticsearch([{'host':'127.0.0.1', 'port': 9200}])

search_body = {
    "size" : 0,
    "aggs" : {
        "trips_per_day" : {
            "date_histogram" : {
                "field" : "pickup_datetime",
                "calendar_interval" : "day"
            }
        }
    }
}

result = es.search(index="taxi", body=search_body)
print("Taxi trips per date: ", json.dumps(result, indent=1))

search_body = {
    "size" : 0,
    "aggs" : {
        "trips_per_day" : {
            "date_histogram" : {
                "field" : "pickup_datetime",
                "calendar_interval" : "day"
            },
            "aggs" : {
                "statistics_of_amount" : {
                    "stats": {"field" : "total_amount"}
                }
            }
        }
    }
}

result = es.search(index="taxi", body=search_body)
print("Statistics per date: ",  json.dumps(result, indent=1))

search_body = {
    "size" : 0,
    "query": {
      "range": {
        "total_amount": {
          "gte": 0,
          "lte": 9999
        }
      }
    },
    "aggs" : {
        "trips_per_day" : {
            "date_histogram" : {
                "field" : "pickup_datetime",
                "calendar_interval" : "day"
            },
            "aggs" : {
                "statistics_of_amount" : {
                    "stats": {"field" : "total_amount"}
                }
            }
        }
    }
}

result = es.search(index="taxi", body=search_body)
print("Corrected statistics per date: ", json.dumps(result, indent=1))

search_body = {
    "size" : 0,
    "query": {
      "range": {
        "total_amount": {
          "gte": 0,
          "lte": 9999
        }
      }
    },
    "aggs" : {
        "trips_per_day" : {
            "terms" : {
                "script" : {
                    "lang": "painless",
                    "source": "doc['pickup_datetime'].value.dayOfWeek"
                }
            },
            "aggs" : {
                "statistics_of_amount" : {
                    "stats": {"field" : "total_amount"}
                }
            }
        }
    }
}

result = es.search(index="taxi", body=search_body)
print("Corrected statistics per day of week: ", json.dumps(result, indent=1))
