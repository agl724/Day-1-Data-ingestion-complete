import pandas as pd
import os

folder = "data/raw"

dataframes = {}

for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)
        df = pd.read_csv(path)
        dataframes[file] = df

        print("\n-----------------")
        print("File:", file)
        print("Shape:", df.shape)
        print(df.head())
