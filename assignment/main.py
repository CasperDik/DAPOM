from load_data import load_data
from visualize_forecasted_deliveries import plot_forecasts

def execute():
    password_elasticsearch = "."
    # load_data(password_elasticsearch)
    print(load_data().help())

    plot_forecasts(password_elasticsearch)


if __name__ == '__main__':
    execute()

    # es.indices.delete(index='taxi', ignore=[400, 404])
