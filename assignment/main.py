from load_data import load_data
from visualize_forecasted_deliveries import plot_locations, descriptivestat_forecast

def execute():
    password_elasticsearch = "."        # remove password before commit

    # load the relevant data
    # load_data(password_elasticsearch)

    # plot the locations on a folium map
    plot_locations(password_elasticsearch)

    # compute descriptive statistics and create a bar chart for total deliveries per district
    descriptivestat_forecast(password_elasticsearch)

if __name__ == '__main__':
    execute()

    # es.indices.delete(index='.', ignore=[400, 404])


# questions:
# -still unsure about total average (daily) deliveries