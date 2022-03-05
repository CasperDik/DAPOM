# Dapom Week 4 Practical B Assignment
# Wout van Wezel, 2020

from elasticsearch import Elasticsearch
import json
import smopy
import folium
import sys, os

es =Elasticsearch([{'host':'127.0.0.1', 'port': 9200}])
# define the query
search_body = {
  "size": 10000,
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_distance": {
          "distance": "100m",
          "pickup_location": {
            "lon": -73.84300994873047,
            "lat": 40.71905517578125
          }
        }
      }
    }
  }
}
result =es.search(index="taxi", body=search_body)
print(json.dumps(result, indent=4))
# have a look at this above result also
print("Hits: ", result["hits"]["total"]["value"])
# Find the minimum and maximum longitude and lattitude
# to sepcify the rectangle that Smopy should display

minLon=9999
minLat=9999
maxLon=-9999
maxLat=-9999
for hit in result["hits"]["hits"]:
    #print(hit["_source"]["pickup_location"])
    point = hit["_source"]["pickup_location"]
    if point[0]<minLon: minLon=point[0]
    if point[1]<minLat: minLat=point[1]
    if point[0]>maxLon: maxLon=point[0]
    if point[1]>maxLat: maxLat=point[1]
# print(minLon,minLat,maxLon,maxLat)
map = smopy.Map(minLat, minLon, maxLat, maxLon, z=15)
ax = map.show_mpl(figsize=(10, 10))

for hit in result["hits"]["hits"]:
    #print(hit["_source"]["pickup_location"])
    point = hit["_source"]["pickup_location"]
    amount = hit["_source"]["total_amount"]
    x, y = map.to_pixels(point[1], point[0])
    #ax.plot(x, y, 'or', ms=4, mew=4);
    if amount<10:
        ax.plot(x, y, 'or', color="red", ms=4, mew=4);
    if amount>=10 and amount<=20:
        ax.plot(x, y, 'or', color="blue", ms=4, mew=4);
    if amount>20:
        ax.plot(x, y, 'or', color="yellow", ms=4, mew=4);
# and now in folium
m = folium.Map(
    location=[40.71905517578125, -73.84300994873047],
    zoom_start=14
)

# Create a zoomable map using Folium.
# mark the circles of picks with the pickup_datetime
# these are visible as labels when clicking on the circles

for hit in result["hits"]["hits"]:
    #print(hit["_source"]["pickup_location"])
    point = hit["_source"]["pickup_location"]
    amount = hit["_source"]["total_amount"]
    if amount<10:
        color="red"
    if amount>=10 and amount<=20:
        color="blue"
    if amount>20:
        color="yellow"
    folium.Circle(
        radius=5,
        location=[point[1], point[0]],
        popup = hit["_source"]["pickup_datetime"],
        color=color,
        fill=False,
    ).add_to(m)

m.save(os.path.join(sys.path[0], "taxiPicks 40.71905517578125-73.84300994873047.html"))

print("exit code 0")
