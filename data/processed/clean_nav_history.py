import pandas as pd

# Reading the file
df = pd.read_csv("data/raw/02_nav_history.csv")

# Parsing  dates
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

df['day']        = df['date'].dt.day
df['month']      = df['date'].dt.month
df['quarter']    = df['date'].dt.quarter
df['year']       = df['date'].dt.year
df['is_weekend'] = df['date'].dt.dayofweek >= 5


# Sorting
df = df.sort_values(["amfi_code", "date"])

# Forward-fill missing NAV (holidays/weekends)
df = df.set_index("date").groupby("amfi_code")["nav"].resample("D").last().ffill().reset_index()

# Remove duplicates
df = df.drop_duplicates(subset=["amfi_code", "date"])

# Validate NAV > 0
df = df[df["nav"] > 0]

df.to_csv("data/processed/clean_nav_history.csv", index=False)
print("Cleaned and saved!", len(df))