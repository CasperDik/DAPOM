from Load_Data import load_data
from Data_Analysis import plot_all_locations, descriptive_statistics_forecast_data
from Locker_Network_Optimization import optimizing_locker_network, plot_results, W_matrix, sensitivity_analysis
import pickle
import pandas as pd
from Locker_Network_Optimization_Bonus import optimizing_locker_network_bonus, plot_network_bonus

def execute():
    password_elasticsearch = "stoepie35"        # remove password before commit

    # load the relevant data
    # load_data(password_elasticsearch)

    # open pickle for colormap
    districts = pickle.load(open("pickles/districts.p", "rb"))

    # plot the locations on a folium map
    # plot_all_locations(password_elasticsearch, districts)

    # compute descriptive statistics and create a bar chart for total deliveries per district
    # descriptive_statistics_forecast_data(password_elasticsearch)

    # create the W matrix
    max_percentage = 0.35
    W_matrix(password_elasticsearch, districts, max_perc_selfpickup=max_percentage)

    # inputs model
    P = 0.25
    C = 24
    W = pickle.load(open("pickles/W_matrix.p", "rb"))
    Demand = pd.read_pickle("pickles/daily_deliveries_location.p")

    # run the optimization model
    # optimizing_locker_network(districts, P, C, W, Demand, max_percentage)

    # visualize the results
    # results = pickle.load(open("pickles/results.p", "rb"))
    # plot_results(results, districts)

    # max_perc_selfpickup = [x / 100.00 for x in range(10, 45, 5)]
    # sensitivity_analysis(password_elasticsearch, "9723", P, C, Demand, max_perc_selfpickup)

    # bonus part:
    # todo: check/change these values
    # list with locker capacities
    capacities = [6, 12, 18]
    # dictionary with costs as values and locker capacities as keys
    costs = {6: 6, 12: 10, 18: 14}
    # district(s) to optimize
    district = ["9712"]

    # run optimization model with different locker capacities
    optimizing_locker_network_bonus(district, P=P, capacities=capacities, costs=costs, W=W, Demand=Demand, max_percentage=max_percentage)

    # load results and plot results using folium
    results = pickle.load(open("pickles/results_bonus.p", "rb"))
    plot_network_bonus(districts=district, results=results)

if __name__ == '__main__':
    execute()

# es.indices.delete(index='.', ignore=[400, 404])

# todo: solve bonus part with right costs etc
# todo: run entire code to test
