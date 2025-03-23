import pandas as pd

def analyze_data(file_path):
    df = pd.read_csv(file_path)
    print(df.describe())
    print(df.head())

analyze_data("data.csv")

# CodeBot_Tracking
