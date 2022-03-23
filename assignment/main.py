from load_data import load_data
from visualize_forecasted_deliveries import plot_locations, descriptivestat_forecast
from optimize_network import optimization_model, plot_results, W_matrix, sensitivity_analysis
import pickle
import pandas as pd

def execute():
    password_elasticsearch = "."        # remove password before commit

    # load the relevant data
    #load_data(password_elasticsearch)

    # open pickle for colormap
    districts = pickle.load(open("pickles/districts.p", "rb"))

    # plot the locations on a folium map
    #plot_locations(password_elasticsearch, districts)

    # compute descriptive statistics and create a bar chart for total deliveries per district
    #descriptivestat_forecast(password_elasticsearch)

    # create the W matrix
    #max_percentage = 0.35
    #W_matrix(password_elasticsearch, districts, max_perc_selfpickup=max_percentage)

    # inputs model
    P = 0.25
    C = 24
    W = pickle.load(open("pickles/W_matrix.p", "rb"))
    Demand = pd.read_pickle("pickles/daily_deliveries_location.p")

    # run the optimization model
    #optimization_model(districts, P, C, W, Demand, max_percentage)

    # visualize the results
    #results = pickle.load(open("pickles/results.p", "rb"))
    #plot_results(results, districts)

    # todo: change to district with highest forecast
    max_perc_selfpickup = [x / 100.00 for x in range(10, 45, 5)]
    sensitivity_analysis(password_elasticsearch, "9723", P, C, Demand, max_perc_selfpickup)


if __name__ == '__main__':
    execute()

    # es.indices.delete(index='.', ignore=[400, 404])

# todo: check gurobi model and inputs
# todo: do some layout for plotting (add stuff and colours etc)
# todo: better naming functions, outputs, files

# todo: do bonus part
# todo: build in try, except, raise stuff
# todo: to classes? --> research layout etc --> only do if I can do it very well
# todo: learn query


# questions:
# - willingness 0 on diagonal?
# - prevent exit code sensitivity
