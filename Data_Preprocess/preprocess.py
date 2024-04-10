import pandas as pd

def preprocess():
    df = pd.read_csv('../data/Mumbai_House_Price.csv')
    print(df.head(5))

preprocess()