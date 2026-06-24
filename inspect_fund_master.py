import pandas as pd
import jupyter

fm = pd.read_csv("data/raw/01_fund_master.csv")

print("Fund Houses:", fm["fund_house"].unique())
print("Categories:", fm["category"].unique())
print("Sub-categories:", fm["sub_category"].unique())
print("Risk grades:", fm["risk_category"].unique())
print("Fund houses count:", fm["fund_house"].nunique())
print("Categories count:", fm["category"].nunique())
print("Sub-categories count:", fm["sub_category"].nunique())
print("Risk grades count:", fm["risk_category"].nunique())
