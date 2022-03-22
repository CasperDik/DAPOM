from load_data import load_data
from visualize_forecasted_deliveries import plot_locations, descriptivestat_forecast

def execute():
    password_elasticsearch = "."        # remove password before commit

    # load the relevant data
    # load_data(password_elasticsearch)

    # plot the locations on a folium map
    # plot_locations(password_elasticsearch)

    # compute descriptive statistics and create a bar chart for total deliveries per district
    # descriptivestat_forecast(password_elasticsearch)

if __name__ == '__main__':
    execute()

    # es.indices.delete(index='.', ignore=[400, 404])
# todo: network stuff --> put in functions and call using main also add weights, demand etc as input? --> easier to do sensitivity
# todo: make pickle with district list and implement everywhere
# todo: import network file and functions from main
# todo: better naming of functions etc and comments and docsstring
# todo: do some layout for plotting (add stuff and colours etc)

# todo: check gurobi model
# todo: do sensitivity
# todo: improve code make nicer --> naming, comments, better code,

# questions:
# - The number of daily forecasted grocery bag deliveries at the ith location is Di --> use the average?
