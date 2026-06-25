import pandas as pd
df = pd.read_csv("data/raw/08_investor_transactions.csv")

# Standardise transaction_type
type_map = {
    "sip": "SIP", "Sip": "SIP",
    "lumpsum": "Lumpsum", "Lump Sum": "Lumpsum", "LUMPSUM": "Lumpsum",
    "redemption": "Redemption", "REDEMPTION": "Redemption", "redeem": "Redemption" 
}
df["transaction_type"] = df["transaction_type"].str.strip().map(type_map)
 # Validate amount > 0
df = df[df["amount_inr"] > 0]

# Fix date formats
df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=True, errors="coerce")

# Validate KYC status
valid_kyc = ["Verified", "Pending"]
df = df[df["kyc_status"].isin(valid_kyc)]

df.to_csv("data/processed/clean_investor_transactions.csv", index=False)
print("Cleaned and saved")