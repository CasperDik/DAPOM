from load_data import load_data
from visualize_forecasted_deliveries import plot_locations, descriptivestat_forecast

def execute():
    password_elasticsearch = "stoepie35"        # remove password before commit
    # load_data(password_elasticsearch)

    # plot_locations(password_elasticsearch)
    # descriptivestat_forecast(password_elasticsearch)

if __name__ == '__main__':
    execute()

    # es.indices.delete(index='.', ignore=[400, 404])


# questions:
# -exclude holidays from all data also for optimization?
# still unsure about total average (daily) deliveries