from elasticsearch import Elasticsearch
import time
from Assignment.loader import ingest_csv_file_into_elastic_index
import pandas as pd
import pickle


def load_data(password_elasticsearch):
    """
    Connects to Elasticsearch and loads the data of the 3 .csv files using the function "load_to_es". Requires your
    elasticsearch password as input. Before uploading does data preparations on 2 files using the function
     data_preparations()
    """
    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # todo: delete
    es.indices.delete(index='assignment_geo_coords', ignore=[400, 404])
    es.indices.delete(index='assignment_distances', ignore=[400, 404])
    es.indices.delete(index='assignment_forecasts23', ignore=[400, 404])

    # for the geo_coordinates and forecast data some data preparation must be done before uploading to elasticsearch
    data_preparations()

    # set mapping and upload geo coords to elasticsearch
    mapping_location = {"properties":
                            {"postcode": {"type": "text"},
                             "lats": {"type": "float"},
                             "longs": {"type": "float"},
                             }
                        }
    upload_to_ES(es, filename="input_data/geo_coordinates_per_each_location_cleaned.csv",
                 index_name="assignment_geo_coords", buffer_size=5000, mapping=mapping_location)

    # set mapping and upload forecasts to elasticsearch
    mapping_forecast = {"properties":
                            {"postcode": {"type": "string"},
                             "cost": {"type": "float"},
                             "date": {"type": "date", "format": "yyyy-MM-dd"}
                             }
                        }
    upload_to_ES(es, filename="input_data/forecasts_2023_cleaned.csv", index_name="assignment_forecasts23",
                 buffer_size=15000, mapping=mapping_forecast)

    # todo: try this upload with mapping once
    # set mapping and upload distances to elasticsearch
    mapping_distances = {"properties":
                             {"start_point_travel": {"type": "string"},
                              "end_point_travel": {"type": "string"},
                              "distance_in_meters": {"type": "float"},
                              "travel_time_on_bike_in_seconds": {"type": "float"}
                              }
                         }
    upload_to_ES(es, filename="input_data/distances_between_locations.csv", index_name="assignment_distances",
                 buffer_size=150000, mapping=mapping_distances)


def data_preparations():
    """data preparations on geo_coordinates and forecast csv files"""

    # load both datasets in pandas
    location_data = pd.read_csv("input_data/geo_coordinates_per_each_location.csv")
    forecast_data = pd.read_csv("input_data/forecasts_2023.csv")

    # rename the columns for both datasets for convenience
    location_data = location_data.rename(
        columns={"postcode_in_Groningen": "postcode", "latitude_North": "lats", "longitude_East": "longs"})
    forecast_data = forecast_data.rename(
        columns={"forecasted year": "year", "cost of the groceries ordered": "cost", "postcode-6-char": "postcode"})

    # create na list with all district locations and store in pickle
    districts = location_data["postcode"].str[:4].drop_duplicates().to_list()
    pickle.dump(districts, open("pickles/districts.p", "wb"))

    # data transformations for forecast dataset:
    # change cost from string to float
    forecast_data["cost"] = pd.to_numeric(forecast_data["cost"].str[4:], downcast="float")

    # replace the months to index of months
    months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
              "September": 9, "October": 10, "November": 11, "December": 12}
    # todo: to numeric needed here?
    forecast_data["month"] = pd.to_numeric(forecast_data["month"].replace(months))

    # remove the 29th of February 2023 from data as it does not exist
    forecast_data = forecast_data[(forecast_data["day"] != 29) & (forecast_data["month"] != 2)]

    # create new column "date", and drop day, month, year, minute, hour columns
    forecast_data["date"] = pd.to_datetime(forecast_data[["year", "month", "day"]], format="%Y/%m/%d")
    forecast_data = forecast_data.drop(["day", "month", "year", "minute", "hour"], axis=1)

    # save both cleaned dataframes as csv
    location_data.to_csv("input_data/geo_coordinates_per_each_location_cleaned.csv", index=False)
    forecast_data.to_csv("input_data/forecasts_2023_cleaned.csv", index=False)


def upload_to_ES(elastic_client: Elasticsearch, filename: str, index_name: str, buffer_size=None, mapping=None):
    """
    Creates a new index in Elasticsearch and uploads the data of a .csv to it. Mapping can be specified but is not
    required.
    """
    tic = time.time()

    # create new index in elasticsearch
    elastic_client.indices.create(index=index_name, ignore=400, mappings=mapping)

    # load csv in index using loader.py
    ingest_csv_file_into_elastic_index(csv_file_name=filename, elastic_client=elastic_client, index_name=index_name,
                                       buffer_size=buffer_size)

    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of loading ', index_name, ': {:.2f} seconds'.format(elapsed_time))
