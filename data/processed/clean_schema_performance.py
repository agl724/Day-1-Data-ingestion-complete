import pandas as pd

df = pd.read_csv("data/raw/07_schema_performance.csv")

# Validateing return columns are numberic
return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]
for col in return_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Flag anomalies ( return outside -50% and -100% are suspicious)
for col in return_cols:
    df["{col}_anomaly"] = -df[col].between(-50, 100)

df["expense_ratio_valid"] = df["expense_ratio_pct"].between(0.1, 2.5)

df.to_csv("data/processed/clean_schema_performance.csv", index=False)

