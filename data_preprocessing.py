import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# exchange csv file to dataframe
dt = pd.read_csv('data/Mumbai_House_Price.csv')


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    for index in df.index:
        price = df.loc[index, 'price']
        price_unit = df.loc[index, 'price_unit']

        # Process price
        if price_unit == 'Cr':
            df.loc[index, 'price_in_USD'] = (price * 10000000 * 0.012)
        elif price_unit == 'L':
            df.loc[index, 'price_in_USD'] = (price * 100000 * 0.012)

        # Process type  ( Apartment: 0, Independent House: 1, Studio Apartment: 2, villa: 3 )
        if df.loc[index, 'type'] == "Apartment":
            df.loc[index, 'house_type'] = int(0)
        elif df.loc[index, 'type'] == "Independent House":
            df.loc[index, 'house_type'] = int(1)
        elif df.loc[index, 'type'] == "Studio Apartment":
            df.loc[index, 'house_type'] = int(2)
        else:
            df.loc[index, 'house_type'] = int(3)

        # Process status ( Ready to move: 0, under Construction: 1 )
        if df.loc[index, 'status'] == "Ready to move":
            df.loc[index, 'status'] = 0
        else:
            df.loc[index, 'status'] = 1

    # Set status to int
    df['status'] = df['status'].astype(int)

    # Set house type to int
    df['house_type'] = df['house_type'].astype(int)

    # Drop unnecessary columns
    df.drop(['price_unit', 'price', 'locality', 'type'], axis = 1, inplace = True)

    # Drop rows that have unknown value
    df = df.replace("Unknown", value = np.NaN)
    df = df.dropna()

    # df = pd.concat([df, dummies.drop('other', axis='columns')], axis='columns')

    # print((type(df.loc[1, 'house_type'])))
    # print(df.head(10)[['region']])
    # print(list(df.columns))
    # print(df.shape)
    return df


def remove_std_outliers(df) -> pd.DataFrame:
    # Add column price per square feet to process data
    df['price_per_sqft'] = df['price_in_USD'] / df['area']
    result_df = pd.DataFrame()
    for index, row in df.groupby('region'):
        mn = np.mean(row['price_per_sqft'])
        std = np.std(row['price_per_sqft'])
        accpt_dt = row[(row['price_per_sqft'] > (mn - std)) & (row['price_per_sqft'] <= (mn + std))]
        result_df = pd.concat([result_df, accpt_dt], ignore_index = True)
    result_df = result_df.drop(['price_per_sqft'], axis = 1)
    return result_df


def process_region(df) -> pd.DataFrame:
    df.region = df.region.apply(lambda x: x.strip())
    region_stats = df['region'].value_counts(ascending=False)
    region_stats_less_than_10 = region_stats[region_stats <= 10]
    df['region'] = df['region'].apply(lambda x: 'other' if x in region_stats_less_than_10 else x)
    return df


def process_age(df) -> pd.DataFrame:
    # Process new column ( if 1 then that house is new else it is resale)
    df['new'] = df.age.apply(lambda x: 1 if x == "New" else 0)
    df = df.drop(['age'], axis = 1)
    idx = df[df['region'] == 'other'].index
    df = df.drop(idx)
    return df


# Convert DataFrane to csv file
def insert_data(df):
    df.to_csv('data/processed_data_1.csv', index = False)


if __name__ == '__main__':
    dt = preprocess(dt)
    dt = process_region(dt)
    dt = remove_std_outliers(dt)
    dt = process_age(dt)
    insert_data(dt)
    print(dt.shape)
    dt.info()