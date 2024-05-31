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


    return df


# Convert DataFrane to csv file
def insert_data(df):
    label_encoder = LabelEncoder()
    df['region'] = label_encoder.fit_transform(df['region'])
    df['locality'] = label_encoder.fit_transform(df['locality'])
    df['type'] = label_encoder.fit_transform(df['type'])
    df['status'] = label_encoder.fit_transform(df['status'])
    df.to_csv('../data/label_encode_raw_processed_data.csv', index = False)


if __name__ == '__main__':
    dt = preprocess(dt)
    insert_data(dt)
    print(dt.shape)
    dt.info()
