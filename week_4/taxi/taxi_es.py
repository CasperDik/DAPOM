from elasticsearch import Elasticsearch
from loaders import ingest_json_file_into_elastic_index
import folium
import time
import branca.colormap as cm
from folium import plugins

# http://localhost:9200/taxi/_mapping?pretty
# http://localhost:9200/taxi/_count


def load_data(filename: str):
    tic = time.time()

    es.indices.create(index='taxi', ignore=400, mappings={
        "properties": {"pickup_location": {"type": "geo_point"},
                       "pickup_datetime": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                       "dropoff_location": {"type": "geo_point"},
                       "dropoff_datetime": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}}}
                      )

    ingest_json_file_into_elastic_index(json_file_name=filename, elastic_client=es, index_name="taxi")

    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of loading data: {:.2f} seconds'.format(elapsed_time))


def query1(latitude: float, longitude: float):
    search_body = {
     "size": 100,
     "query": {
         "bool": {
             "must": {
                 "match_all": {}
             },
             "filter": {
                 "geo_distance": {
                     "distance": "100m",
                     "pickup_location": {
                         "lat": latitude,
                         "lon": longitude
                     }
                 }
             }
         }
     }
    }

    result = dict(es.search(index="taxi", body=search_body))
    print(result)
    print("query resulted in ", result["hits"]["total"]["value"], "hits")

    coords = [result["hits"]["hits"][i]["_source"]["pickup_location"] for i in range(len(result["hits"]["hits"]))]
    amount = [result["hits"]["hits"][i]["_source"]["total_amount"] for i in range(len(result["hits"]["hits"]))]
    # print(coords)

    return coords, amount

def query_sql():
    amount = es.sql.query(body={"query": "SELECT total_amount FROM taxi WHERE total_amount>10"})
    print(amount)

def plot_cords_as_marker(coords, amount):
    longs = [l[0] for l in coords]
    lats = [l[1] for l in coords]

    m = folium.Map(location=[(min(lats) + max(lats)) / 2, (min(longs) + max(longs)) / 2], zoom_start=15,
                   control_scale=True)

    colormap = cm.LinearColormap(colors=['blue', 'red'], index=[min(amount), max(amount)], vmin=min(amount), vmax=max(amount))

    for lat, long, a in zip(lats, longs, amount):
        folium.Marker([lat, long], popup="taxi ride costed {:.2f} dollars".format(a), icon=folium.Icon(color="white", icon_color=colormap(a)), tooltip="pickup point taxi").add_to(m)

    minimap = plugins.MiniMap()
    m.add_child(minimap)
    m.add_child(colormap)

    m.save("taxi_pickup_locations.html")
    print("folium map completed")

if __name__ == '__main__':
    password = "."
    es = Elasticsearch(hosts="http://elastic:" + password + "@localhost:9200")
    # es.indices.delete(index='taxi', ignore=[400, 404])
    # load_data("taxi-1000000.json")

    # coords, amount = query1(40.71905517578125, -73.84300994873047)
    # plot_cords_as_marker(coords, amount)

    query_sql()