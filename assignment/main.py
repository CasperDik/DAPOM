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

# todo: make pickle with district list and implement everywhere
# todo: retrieve relevant data gurobi model --> put everything in dict first then pickle?
# todo: network stuff --> put in functions and call using main
# todo: check gurobi model
# todo: plot locations (read assignment first)

# questions:
# - still unsure about total average (daily) deliveries
# - how to add html file to assignment document
# - The number of daily forecasted grocery bag deliveries at the ith location is Di --> use the average?
# - optimize per district or in total?
