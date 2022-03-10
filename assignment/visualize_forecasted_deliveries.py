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
# todo: add comments and general description

def plot_locations(password_elasticsearch:  str):
    # only query from elasticsearch when the pickle doesn't exist, if it exists load the file
    if os.path.isfile("pickles/assignment_geo_coords.p"):
        locations_data = pd.read_pickle("pickles/assignment_geo_coords.p")
    else:
        query_all_entries(password_elasticsearch, "assignment_geo_coords")
        locations_data = pd.read_pickle("pickles/assignment_geo_coords.p")

    locations_data = locations_data.rename(columns={"postcode_in_Groningen": "postcode", "latitude_North": "lats", "longitude_East": "longs"})
    locations_data["districts"] = locations_data["postcode"].str[:4]

    m = folium.Map(location=[(min(locations_data["lats"]) + max(locations_data["lats"])) / 2, (min(locations_data["longs"])
                                + max(locations_data["longs"])) / 2], zoom_start=12)

    districts = locations_data["districts"].drop_duplicates().to_list()
    cmap = mcp.gen_color(cmap="tab20b", n=len(districts))
    color_dict = dict(zip(districts, cmap))

    # todo: add forecast and 6 letter postcode to popup
    for lat, long, a in zip(locations_data["lats"], locations_data["longs"], locations_data["districts"]):
        folium.CircleMarker(location=(lat, long), radius=2, color=color_dict.get(a), popup="district " + a).add_to(m)

    m.save("locations.html")

def descriptivestat_forecast(password_elasticsearch: str):
    # only query from elasticsearch when the pickle doesn't exist, if it exists load the file
    if os.path.isfile("pickles/assignment_forecasts23.p"):
        forecast_data = pd.read_pickle("pickles/assignment_forecasts23.p")
    else:
        query_all_entries(password_elasticsearch, "assignment_forecasts23")
        forecast_data = pd.read_pickle("pickles/assignment_forecasts23.p")

    # rename columns
    forecast_data = forecast_data.rename(columns={"forecasted year": "year", "cost of the groceries ordered": "cost", "postcode-6-char": "postcode"})

    # costs that to usable float
    forecast_data["cost"] = pd.to_numeric(forecast_data["cost"].str[4:], downcast="float")

    # replace months with index of the month
    months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
              "September": 9, "October": 10, "November": 11, "December": 12}
    forecast_data["month"] = pd.to_numeric(forecast_data['month'].replace(months))

    # exclude 29th of feb for 2023 since not leap year
    forecast_data = forecast_data[(forecast_data["day"] != 29) & (forecast_data["month"] != 2)]

    # create date variable
    forecast_data["date"] = pd.to_datetime(forecast_data[["year", "month", "day"]], format="%Y/%m/%d")

    # create list with holidays to exclude
    holidays_to_exclude = list(dict(holidays.NL(years=2023).items()).keys())
    # exclude all holidays
    forecast_data = forecast_data[~forecast_data["date"].isin(holidays_to_exclude)]

    # compute average deliveries per location
    avg_d_deliveries_location = forecast_data.groupby(["date", "postcode"])["cost"].mean()
    print(avg_d_deliveries_location.head())

    # get districts
    forecast_data["district"] = forecast_data["postcode"].str[:4]
    # compute total daily average deliveries for each district
    avg_d_deliveries_district = forecast_data.groupby(["date", "district"])["cost"].mean()
    print(avg_d_deliveries_district.head())

    # todo: Plot total average deliveries for each district on a bar chart. The graph will have as many bars as the number of districts
    avg_deliveries_district = forecast_data.groupby("district")["cost"].mean()
    print(len(avg_deliveries_district))
    plt.bar(forecast_data["district"].drop_duplicates(), avg_deliveries_district)
    plt.show()

    print("x")






