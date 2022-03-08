from elasticsearch import Elasticsearch
import json

password = "."
es = Elasticsearch(hosts="http://elastic:" + password + "@localhost:9200")

search_body_count_per_day = {
    "size": 0,
    "aggs": {
        "count_per_day": {
           "date_histogram": {
               "field": "pickup_datetime",
               "calendar_interval": "day"
           }
        }
    }
}

search_body_total_amount_per_day = {
    "size": 0,
    "aggs": {
        "count_per_day": {
           "date_histogram": {
               "field": "pickup_datetime",
               "calendar_interval": "day"
           },
            "aggs": {
                "total_amount_pd": {
                    "stats": {"field": "total_amount"},
                    }
                }
            }
        }
    }


# todo: fix this query
search_body_total_amount_per_day_with_filter = {
    "size": 0,
    "query": {
        "range": {
            "total_amount": {
                "gte": 0,
                "lte:": 9999
            }
        }
    },
    "aggs": {
        "count_per_day": {
           "date_histogram": {
               "field": "pickup_datetime",
               "calendar_interval": "day"
                }
           },
            "aggs": {
                "total_amount_pd": {
                    "stats": {"field": "total_amount"},
                    }
                }
            }
        }



result = es.search(index="taxi", body=search_body_total_amount_per_day_with_filter)
print(json.dumps(dict(result), indent=1))
