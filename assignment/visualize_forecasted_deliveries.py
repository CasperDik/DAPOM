import folium
from es_queries import query_all_entries
from mycolorpy import colorlist as mcp
import pandas as pd
from datetime import date
import holidays
import calendar
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
    """compute and plot descriptive statistics for the forecast data retrieved from elasticsearch"""
    # todo: can also do this directly via elasticsearch? if time

    # only query from elasticsearch when the pickle file doesn't exist, if it exists load the pickle file
    if os.path.isfile("pickles/assignment_forecasts23.p"):
        forecast_data = pd.read_pickle("pickles/assignment_forecasts23.p")
    else:
        query_all_entries(password_elasticsearch, "assignment_forecasts23")
        forecast_data = pd.read_pickle("pickles/assignment_forecasts23.p")

    # create list with holidays to exclude
    holidays_to_exclude = list(dict(holidays.NL(years=2023).items()).keys())
    # exclude all holidays
    forecast_data = forecast_data[~forecast_data["date"].isin(holidays_to_exclude)]

    # compute forecasted daily average deliveries per location
    avg_d_deliveries_location = forecast_data.groupby(["postcode"])["cost"].count().div(365)
    print(avg_d_deliveries_location.head())

    # get districts
    forecast_data["district"] = forecast_data["postcode"].str[:4]

    # compute total daily average deliveries for each district
    avg_d_deliveries_district = forecast_data.groupby(["district"])["cost"].count().div(365)
    print(avg_d_deliveries_district.head())

    # compute total average deliveries for each district
    # todo: is this correct --> it is now total deliveries per district but needs some average? of what? per day?
    avg_deliveries_district = forecast_data.groupby(["district"])["cost"].count()

    # plot on a bar chart
    # todo: add (axis) titles and ylim
    # plt.ylim([41.5, max(avg_deliveries_district)])
    plt.xticks(rotation='vertical')
    plt.bar(forecast_data["district"].drop_duplicates(), avg_deliveries_district)
    plt.show()

    plt.savefig("outputs/bar_plot_deliveries.png")







