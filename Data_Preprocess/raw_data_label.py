import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder

# exchange csv file to dataframe
dt = pd.read_csv('../data/Mumbai_House_Price.csv')


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
    df = df.replace("Unknown", np.NaN)
    df = df.dropna()

    # df = pd.concat([df, dummies.drop('other', axis='columns')], axis='columns')

    # print((type(df.loc[1, 'house_type'])))
    # print(df.head(10)[['region']])
    # print(list(df.columns))
    # print(df.shape)
    return df


# Convert DataFrane to csv file
def insert_data(df):
    label_encoder = LabelEncoder()
    df['region'] = label_encoder.fit_transform(df['region'])
    df.to_csv('../data/label_encode_raw_processed_data.csv', index = False)


if __name__ == '__main__':
    dt = preprocess(dt)
    insert_data(dt)
    print(dt.shape)
    dt.info()
