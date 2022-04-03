import folium
from ES_queries import query_all_entries, query_locations_count, query_district_count
from mycolorpy import colorlist as mcp
import pandas as pd
import holidays
import os
import matplotlib.pylab as plt
import random

def plot_all_locations(password_elasticsearch:  str, districts: list):
    """plot the locations using folium and the data from elasticsearch"""

    # only query from elasticsearch when the file pickle doesn't exist, if it exists load the pickle file
    if os.path.isfile("pickles/assignment_geo_coords.p"):
        location_data = pd.read_pickle("pickles/assignment_geo_coords.p")
    else:
        query_all_entries(password_elasticsearch, "assignment_geo_coords")
        location_data = pd.read_pickle("pickles/assignment_geo_coords.p")

    # initiate the map
    m = folium.Map(location=[(min(location_data["lats"]) + max(location_data["lats"])) / 2, (min(location_data["longs"])
                                + max(location_data["longs"])) / 2], zoom_start=13)
    # add custom map tile
    folium.TileLayer(
        tiles='https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
        ).add_to(m)

    # create a colormap of the length of the list of districts
    cmap = mcp.gen_color(cmap="tab20b", n=len(districts))
    random.shuffle(cmap)
    # create a dictionary were every district is linked to a column
    color_dict = dict(zip(districts, cmap))

    # plot a circle for each location on the folium map
    for lat, long, a in zip(location_data["lats"], location_data["longs"], location_data["postcode"].str[:4]):
        folium.CircleMarker(location=(lat, long), radius=2, color=color_dict.get(a), popup="district " + str(a)).add_to(m)

    # save folium map as html
    m.save("outputs/all_locations_with_colours.html")


def descriptive_statistics_forecast_data(password_elasticsearch: str):
    """computes descriptive statistics using elasticsearch and pandas"""

    # create list with holidays to exclude
    Holidays = list(dict(holidays.NL(years=2023).items()).keys())
    holiday_to_exclude = []

    # loop over this list to create part of the query that excludes the holidays
    for holiday in Holidays:
        holiday_to_exclude.append({
            "range": {
                "delivery_data": {
                    "gte": holiday,
                    "lte": holiday,
                    "format": "yyyy-MM-dd"
                }
            }
        })

    # run the query to get the count per location and store in dataframe
    location = pd.DataFrame(query_locations_count(password_elasticsearch, holiday_to_exclude))
    # create new column with average daily deliveries per location
    location["avg_daily_location"] = location["doc_count"].div(365)
    # sort based on postcode
    location.sort_values("key", inplace=True)
    print("Average daily deliveries per location: \n", location.head())
    # store data as pickle to use later
    location.to_pickle("pickles/daily_deliveries_location.p")

    # run the query with the previously created search body and store in new dataframe
    district = pd.DataFrame(query_district_count(password_elasticsearch, holiday_to_exclude))
    # get average daily deliveries per district
    district["avg_daily_district"] = district["doc_count"].div(365)
    district.sort_values("key", inplace=True)
    print("Average daily deliveries per district: \n", district.head())

    # plot on a bar chart
    plt.title("Average Daily Deliveries per District")
    plt.xlabel("Districts")
    plt.ylabel("Average Daily Deliveries")
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.bar(district["key"], district["avg_daily_district"])
    plt.savefig("outputs/bar_plot_deliveries.png")

    plt.show()
