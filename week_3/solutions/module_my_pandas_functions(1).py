import pandas as pd


def read_big_file(filename: str = "file_argument_missing"):
    df = pd.read_csv(filename, low_memory=False)
    return df


def do_stats_for(df:pd.DataFrame):
    print("the size of the table is (rows * columns):")
    print(df.shape)
    print("the rows are organized as:")
    print(df.columns)
    print("the Python type of the values on the columns are:")
    print(df.dtypes)
    units = df["Units Sold"].mean()
    price = df["Unit Price"].mean()
    cost = df["Unit Cost"].mean()
    print("mean units sold per transaction:", units)
    print("mean price/unit per transaction:", price)
    print("mean cost/unit per transaction:", cost)
    total_calc_profit = units * (price - cost) * df.shape[0]
    print("calculated profit via means:", total_calc_profit)
    total_profit = sum(df['Total Profit'])
    print("Total profit from table:", total_profit)
    print("calculation error is: ", total_profit - total_calc_profit)


def iterate_through_entire(table):
    for row in table.index:
        print(row)

def save_only_Sub_Saharan_Africa(table):
    df = table[table['Region'].str.contains('Sub-Saharan Africa')]
    df.to_csv("onlySubSaharanAfrica.csv")
