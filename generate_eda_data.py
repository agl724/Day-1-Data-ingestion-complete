"""
Extended dataset generator for EDA_Analysis tasks.
Produces: 40-scheme NAV 2022-2026, enriched AUM, monthly SIP inflows,
category heatmap, folio growth, demographics with gender/state, holdings.
"""
import pandas as pd
import numpy as np
from datetime import datetime, date
import random, os

np.random.seed(2024); random.seed(2024)
RAW = "/home/claude/mf_analysis/data/raw"

# ── 40 schemes definition ─────────────────────────────────────────────────────
SCHEMES_40 = [
    # Large Cap (10)
    (119551,"SBI Bluechip","SBI MF","Equity","Large Cap",58.0),
    (120503,"ICICI Pru Bluechip","ICICI Prudential","Equity","Large Cap",42.0),
    (118632,"Nippon Large Cap","Nippon India","Equity","Large Cap",35.0),
    (119092,"Axis Bluechip","Axis MF","Equity","Large Cap",38.0),
    (120841,"Kotak Bluechip","Kotak MF","Equity","Large Cap",36.0),
    (125497,"HDFC Top 100","HDFC MF","Equity","Large Cap",80.0),
    (118825,"Mirae Large Cap","Mirae Asset","Equity","Large Cap",62.0),
    (120465,"DSP Top 100","DSP MF","Equity","Large Cap",44.0),
    (119775,"UTI Mastershare","UTI MF","Equity","Large Cap",150.0),
    (118989,"ABSL Frontline","Aditya Birla SL","Equity","Large Cap",310.0),
    # Mid Cap (8)
    (120700,"HDFC Midcap Opp","HDFC MF","Equity","Mid Cap",55.0),
    (119802,"Kotak Emerging","Kotak MF","Equity","Mid Cap",72.0),
    (118778,"Nippon Growth","Nippon India","Equity","Mid Cap",2100.0),
    (120211,"DSP Midcap","DSP MF","Equity","Mid Cap",88.0),
    (119444,"SBI Magnum Midcap","SBI MF","Equity","Mid Cap",160.0),
    (120988,"Axis Midcap","Axis MF","Equity","Mid Cap",64.0),
    (119630,"UTI Mid Cap","UTI MF","Equity","Mid Cap",210.0),
    (118560,"Mirae Emerging","Mirae Asset","Equity","Mid Cap",90.0),
    # Small Cap (6)
    (120100,"Nippon Small Cap","Nippon India","Equity","Small Cap",95.0),
    (119900,"SBI Small Cap","SBI MF","Equity","Small Cap",130.0),
    (120300,"HDFC Small Cap","HDFC MF","Equity","Small Cap",88.0),
    (118400,"Kotak Small Cap","Kotak MF","Equity","Small Cap",160.0),
    (119200,"Axis Small Cap","Axis MF","Equity","Small Cap",55.0),
    (120600,"ICICI Small Cap","ICICI Prudential","Equity","Small Cap",45.0),
    # Flexi Cap (4)
    (119350,"Parag Parikh Flexi","PPFAS","Equity","Flexi Cap",52.0),
    (120450,"HDFC Flexi Cap","HDFC MF","Equity","Flexi Cap",1380.0),
    (119650,"ICICI Flexi Cap","ICICI Prudential","Equity","Flexi Cap",14.0),
    (118750,"UTI Flexi Cap","UTI MF","Equity","Flexi Cap",230.0),
    # ELSS (4)
    (119100,"Axis ELSS","Axis MF","Equity","ELSS",28.0),
    (120200,"Mirae ELSS","Mirae Asset","Equity","ELSS",32.0),
    (118300,"DSP ELSS","DSP MF","Equity","ELSS",90.0),
    (120500,"Canara ELSS","Canara Robeco","Equity","ELSS",120.0),
    # Debt (4)
    (101001,"HDFC Liquid","HDFC MF","Debt","Liquid",3500.0),
    (101002,"SBI Liquid","SBI MF","Debt","Liquid",3200.0),
    (101003,"ICICI Short Dur","ICICI Prudential","Debt","Short Duration",22.0),
    (101004,"Kotak Corp Bond","Kotak MF","Debt","Medium Duration",28.0),
    # Hybrid (4)
    (102001,"ICICI Balanced Adv","ICICI Prudential","Hybrid","Balanced Advantage",55.0),
    (102002,"HDFC Balanced Adv","HDFC MF","Hybrid","Balanced Advantage",73.0),
    (102003,"SBI Equity Hybrid","SBI MF","Hybrid","Aggressive Hybrid",210.0),
    (102004,"Kotak Equity Hybrid","Kotak MF","Hybrid","Aggressive Hybrid",42.0),
]

FUND_HOUSES = sorted(set(s[2] for s in SCHEMES_40))
CATEGORIES  = sorted(set(s[3] for s in SCHEMES_40))

# ── NAV history 2022-01-03 to 2026-03-28 ─────────────────────────────────────
dates = pd.bdate_range("2022-01-03","2026-03-28")

# Market regime multipliers (daily drift adjustments by period)
def get_regime(d):
    if d < pd.Timestamp("2022-06-01"):   return -0.0004   # correction
    if d < pd.Timestamp("2023-01-01"):   return  0.0001   # recovery
    if d < pd.Timestamp("2023-12-31"):   return  0.0007   # 2023 bull run
    if d < pd.Timestamp("2024-03-01"):   return  0.0004   # election rally
    if d < pd.Timestamp("2024-09-01"):   return -0.0003   # 2024 correction
    if d < pd.Timestamp("2025-01-01"):   return  0.0003   # stabilise
    return 0.0005                                          # 2025-26 growth

nav_rows = []
for code,name,house,cat,subcat,nav0 in SCHEMES_40:
    vol = {"Equity":0.013,"Debt":0.001,"Hybrid":0.008}[cat]
    nav = float(nav0)
    for d in dates:
        drift = get_regime(d)
        # debt barely moves
        if cat == "Debt":
            nav = nav * (1 + np.random.normal(0.00025, 0.0003))
        else:
            nav = max(nav * (1 + np.random.normal(drift, vol)), nav0*0.3)
        nav_rows.append({"scheme_code":code,"scheme_name":name,
                          "fund_house":house,"category":cat,"sub_category":subcat,
                          "date":d.date(),"nav":round(nav,4)})

nav_40 = pd.DataFrame(nav_rows)
nav_40.to_csv(f"{RAW}/nav_history_40schemes.csv", index=False)
print(f"nav_history_40schemes: {nav_40.shape}")

# ── AUM by fund house 2022-2025 ───────────────────────────────────────────────
months = pd.date_range("2022-01-01","2025-12-01",freq="MS")
aum_rows = []
# Approx industry AUM starting points (₹ Cr) per fund house
base_aum = {
    "SBI MF":350000,"ICICI Prudential":330000,"HDFC MF":420000,
    "Nippon India":180000,"Axis MF":220000,"Kotak MF":200000,
    "Mirae Asset":120000,"DSP MF":80000,"UTI MF":150000,
    "Aditya Birla SL":280000,"PPFAS":30000,"Canara Robeco":60000,
}
for fh, base in base_aum.items():
    aum = base
    for m in months:
        # SBI crosses 12.5L Cr by 2025
        drift = 0.012 if fh=="SBI MF" else 0.009
        aum = aum * (1 + np.random.normal(drift, 0.03))
        aum = max(aum, base*0.5)
        aum_rows.append({"fund_house":fh,"month":m.date(),
                          "year":m.year,"aum_cr":round(aum,0)})

aum_fh = pd.DataFrame(aum_rows)
aum_fh.to_csv(f"{RAW}/aum_by_fundhouse.csv", index=False)
print(f"aum_by_fundhouse: {aum_fh.shape}")

# ── Monthly SIP inflows Jan 2022 – Dec 2025 ───────────────────────────────────
sip_months = pd.date_range("2022-01-01","2025-12-01",freq="MS")
sip_base = 11000  # Cr in Jan 2022
sip_rows2 = []
for m in sip_months:
    # Steady uptrend with seasonality
    trend = (m.year - 2022)*4200 + (m.month-1)*120
    seasonal = 800 * np.sin(2*np.pi*(m.month-3)/12)
    noise = np.random.normal(0, 300)
    inflow = sip_base + trend + seasonal + noise
    # All-time high Dec 2025 → 31002
    if m.year==2025 and m.month==12:
        inflow = 31002
    sip_rows2.append({"month":m.date(),"year":m.year,
                       "monthly_sip_inflow_cr":round(inflow,1),
                       "sip_accounts_lakh":round(inflow/0.45,0)})

sip_monthly = pd.DataFrame(sip_rows2)
sip_monthly.to_csv(f"{RAW}/sip_monthly_inflow.csv", index=False)
print(f"sip_monthly_inflow: {sip_monthly.shape}")

# ── Category inflow heatmap ───────────────────────────────────────────────────
cats = ["Large Cap","Mid Cap","Small Cap","Flexi Cap","ELSS",
        "Liquid","Short Duration","Balanced Advantage","Aggressive Hybrid","ELSS"]
cats = list(dict.fromkeys(cats))  # dedupe
heat_rows = []
for m in sip_months:
    for cat in cats:
        # Different seasonality per category
        base = {"Large Cap":3500,"Mid Cap":2200,"Small Cap":2000,
                "Flexi Cap":2800,"ELSS":1800 if m.month in [1,2,3] else 600,
                "Liquid":8000,"Short Duration":2500,
                "Balanced Advantage":1200,"Aggressive Hybrid":900}.get(cat,800)
        inflow = base * (1 + 0.003*((m.year-2022)*12+m.month)) + np.random.normal(0, base*0.12)
        heat_rows.append({"month":m.date(),"month_label":m.strftime("%b %Y"),
                           "category":cat,"net_inflow_cr":round(inflow,1)})

heatmap_df = pd.DataFrame(heat_rows)
heatmap_df.to_csv(f"{RAW}/category_inflow_heatmap.csv", index=False)
print(f"category_inflow_heatmap: {heatmap_df.shape}")

# ── Folio count growth (Cr) Jan 2022 – Dec 2025 ──────────────────────────────
folio_rows = []
folio = 13.26
for m in sip_months:
    folio = folio + np.random.normal(0.32, 0.08)
    if m.year==2025 and m.month==12:
        folio = 26.12
    folio_rows.append({"month":m.date(),"folios_cr":round(folio,2)})

folio_df = pd.DataFrame(folio_rows)
folio_df.to_csv(f"{RAW}/folio_count_growth.csv", index=False)
print(f"folio_count_growth: {folio_df.shape}")

# ── Enriched investor profile with gender + state ────────────────────────────
inv = pd.read_csv(f"{RAW}/investor_profile.csv")
STATES_T30 = ["Maharashtra","Delhi","Karnataka","Tamil Nadu","Gujarat",
               "West Bengal","Telangana","Rajasthan","Uttar Pradesh","Kerala"]
STATES_B30 = ["Bihar","Jharkhand","Chhattisgarh","Odisha","Assam",
               "Uttarakhand","Himachal Pradesh","Manipur","Meghalaya","Tripura"]
inv["gender"]      = np.random.choice(["Male","Female","Other"],[len(inv)],p=[0.58,0.40,0.02])
inv["state"]       = [random.choice(STATES_T30) if t=="Tier1" else random.choice(STATES_B30)
                       for t in inv["city_tier"]]
inv["avg_sip_amt"] = np.random.choice([500,1000,2000,3000,5000,10000,25000],
                                       size=len(inv), p=[0.05,0.25,0.28,0.15,0.15,0.08,0.04])
inv.to_csv(f"{RAW}/investor_profile_enriched.csv", index=False)
print(f"investor_profile_enriched: {inv.shape}")

# ── Portfolio holdings across 40 equity schemes ───────────────────────────────
STOCKS = {
    "RELIANCE":{"sector":"Energy","isin":"INE002A01018"},
    "HDFC BANK":{"sector":"Banking & Finance","isin":"INE040A01034"},
    "INFOSYS":{"sector":"IT","isin":"INE009A01021"},
    "ICICI BANK":{"sector":"Banking & Finance","isin":"INE090A01021"},
    "TCS":{"sector":"IT","isin":"INE467B01029"},
    "BHARTI AIRTEL":{"sector":"Telecom","isin":"INE397D01024"},
    "ITC":{"sector":"FMCG","isin":"INE154A01025"},
    "L&T":{"sector":"Capital Goods","isin":"INE018A01030"},
    "AXIS BANK":{"sector":"Banking & Finance","isin":"INE238A01034"},
    "KOTAK MAHINDRA":{"sector":"Banking & Finance","isin":"INE237A01028"},
    "BAJAJ FINANCE":{"sector":"Banking & Finance","isin":"INE296A01024"},
    "HUL":{"sector":"FMCG","isin":"INE030A01027"},
    "MARUTI SUZUKI":{"sector":"Auto","isin":"INE585B01010"},
    "TITAN":{"sector":"Consumer Discretionary","isin":"INE280A01028"},
    "WIPRO":{"sector":"IT","isin":"INE075A01022"},
    "NTPC":{"sector":"Power","isin":"INE733E01010"},
    "ONGC":{"sector":"Energy","isin":"INE213A01029"},
    "POWER GRID":{"sector":"Power","isin":"INE752E01010"},
    "ADANI PORTS":{"sector":"Infrastructure","isin":"INE742F01042"},
    "SBI":{"sector":"Banking & Finance","isin":"INE062A01020"},
    "M&M":{"sector":"Auto","isin":"INE101A01026"},
    "ASIAN PAINTS":{"sector":"Consumer Discretionary","isin":"INE021A01026"},
    "ULTRATECH":{"sector":"Cement","isin":"INE481G01011"},
    "NESTLE":{"sector":"FMCG","isin":"INE239A01016"},
}
equity_codes = [s[0] for s in SCHEMES_40 if s[3]=="Equity"]
hold_rows = []
for code in equity_codes:
    # Each fund picks 15-20 stocks
    n = random.randint(15,20)
    picked = random.sample(list(STOCKS.keys()), n)
    weights = np.random.dirichlet(np.ones(n)*2) * 100
    for stock, w in zip(picked, weights):
        hold_rows.append({"scheme_code":code,"stock_name":stock,
                           "isin":STOCKS[stock]["isin"],"sector":STOCKS[stock]["sector"],
                           "weight_pct":round(w,2),"as_of_date":"2025-12-31"})

holdings_df = pd.DataFrame(hold_rows)
holdings_df.to_csv(f"{RAW}/portfolio_holdings_detailed.csv", index=False)
print(f"portfolio_holdings_detailed: {holdings_df.shape}")

print("\n✅ All EDA datasets ready!")
