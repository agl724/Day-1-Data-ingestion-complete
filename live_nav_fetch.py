import requests
import pandas as pd

#Only for the hdfc top 100
#url =  "https://api.mfapi.in/mf/125497"

#response = requests.get(url)
#data = response.json()

#nav_df = pd.DataFrame(data["data"])
#nav_df.to_csv("data/raw/hdfc_top100_nav.csv", index=False)
#print("saved")

schemas = {
    "SBI Bluechip": 119551,
    "ICICI Bluechip": 120503,
    "Nippon Large Cap": 118632,
    "Axis Bluechip": 119092,
    "Kotak Bluechip": 120841
}
all_data = []
for schema_name, schema_code in schemas.items():
    url = f"https://api.mfapi.in/mf/{schema_code}"
    response = requests.get(url)
    data = response.json()

    nav_df = pd.DataFrame(data["data"])
    nav_df["schema"]= schema_name
    nav_df["schema_Code"] = schema_code

    all_data.append(nav_df)
    print(f"Data fetched {schema_name}")


combined_df = pd.concat(all_data, ignore_index=True)
combined_df.to_csv("data/raw/bluechip_nav.csv", index=False)
print(f"\nSaved {len(combined_df)} NAV records to bluechip_nav.csv")
print(type(schemas))
