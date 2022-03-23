from load_data import load_data
from visualize_forecasted_deliveries import plot_locations, descriptivestat_forecast
from optimize_network import optimization_model, plot_results, W_matrix
import pickle
import pandas as pd

def execute():
    password_elasticsearch = "."        # remove password before commit

    # load the relevant data
    # load_data(password_elasticsearch)

    # open pickle for colormap
    districts = pickle.load(open("pickles/districts.p", "rb"))

    # plot the locations on a folium map
    # plot_locations(password_elasticsearch, districts)

    # compute descriptive statistics and create a bar chart for total deliveries per district
    # descriptivestat_forecast(password_elasticsearch)

    # create the W matrix
    # W_matrix(password_elasticsearch, districts)

    # inputs model
    P = 0.25
    C = 24
    W = pickle.load(open("pickles/W_matrix.p", "rb"))
    Demand = pd.read_pickle("pickles/daily_deliveries_location.p")

    # run the optimization model
    optimization_model(districts, P, C, W, Demand)

    # visualize the results
    results = pickle.load(open("pickles/results.p", "rb"))
    plot_results(results, districts)



if __name__ == '__main__':
    execute()

    # es.indices.delete(index='.', ignore=[400, 404])

# todo: do some layout for plotting (add stuff and colours etc)
# todo: check gurobi model and inputs
# todo: do sensitivity
# todo: improve code make nicer --> naming, comments, better code

# todo: do bonus part
# todo: build in try, except, raise stuff
# todo: to classes? --> research layout etc --> only do if I can do it very well


# questions:
# - The number of daily forecasted grocery bag deliveries at the ith location is Di --> use the average?
