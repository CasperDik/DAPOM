import folium
from es_queries import query_all_entries, query_count_locations, query_count_district
from mycolorpy import colorlist as mcp
import pandas as pd
import holidays
import os
import pickle
import matplotlib.pylab as plt

def plot_locations(password_elasticsearch:  str):
    """plot the locations using folium and the data from elasticsearch"""

    # only query from elasticsearch when the file pickle doesn't exist, if it exists load the pickle file
    if os.path.isfile("pickles/assignment_geo_coords.p"):
        location_data = pd.read_pickle("pickles/assignment_geo_coords.p")
    else:
        query_all_entries(password_elasticsearch, "assignment_geo_coords")
        location_data = pd.read_pickle("pickles/assignment_geo_coords.p")

    # initiate the map
    m = folium.Map(location=[(min(location_data["lats"]) + max(location_data["lats"])) / 2, (min(location_data["longs"])
                                + max(location_data["longs"])) / 2], zoom_start=12)

    # get a list of all the districts without duplicates
    location_data["district"] = location_data["postcode"].str[:4]
    districts = location_data["districts"].drop_duplicates().to_list()
    # create a colormap of the length of the list of districts
    cmap = mcp.gen_color(cmap="tab20b", n=len(districts))   # todo: other colormap?
    # create a dictionary were every district is linked to a column
    color_dict = dict(zip(districts, cmap))

    # todo: add forecast and 6 letter postcode to popup
    # plot a circle for each location on the folium map
    for lat, long, a in zip(location_data["lats"], location_data["longs"], location_data["districts"]):
        folium.CircleMarker(location=(lat, long), radius=2, color=color_dict.get(a), popup="district " + str(a)).add_to(m)

    # save folium map as html
    m.save("outputs/locations.html")


def descriptivestat_forecast(password_elasticsearch: str):
    """add sth.."""
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
    location = pd.DataFrame(query_count_locations(password_elasticsearch, holiday_to_exclude))
    # create new column with average daily deliveries per location
    location["avg_daily_location"] = location["doc_count"].div(365)
    print(location.head())

    # run the query with the previously created search body and store in new dataframe
    district = pd.DataFrame(query_count_district(password_elasticsearch, holiday_to_exclude))
    # get average daily deliveries per district
    district["avg_daily_district"] = district["doc_count"].div(365)
    print(district.head())

    # plot on a bar chart
    # todo: add (axis) titles and ylim + make nicer
    # plt.ylim([41.5, max(avg_deliveries_district)])
    plt.xticks(rotation='vertical')
    plt.bar(district["key"], district["avg_daily_district"])
    plt.savefig("outputs/bar_plot_deliveries.png")

    plt.show()
