CREATE TABLE dim_fund(
    fund_id INT PRIMARY KEY,
    amfi_code INT,
    schema_name TEXT,
    fund_house TEXT,
    category TEXT,
    plan TEXT
);

CREATE TABLE dim_date(
    date_id INT PRIMARY KEY,
    date DATE
);

CREATE TABLE fact_nav(
    nav_id INT PRIMARY KEY AUTOINCREMENT,
    fund_id INT REFERENCES dim_fund(fund_id),
    date_id INT REFERENCES dim_date(date_id),
    nav REAL NOT NULL
);

CREATE TABLE fact_transactions(
    txn_id INT PRIMARY KEY AUTOINCREMENT,
    amfi_code INT,
    investor_id TEXT,
    fund_id INT REFERENCES dim_fund(fund_id),
    date_id INT REFERENCES dim_date(date_id),
    transaction_date DATE,
    transaction_type TEXT CHECK(transaction_type IN ('SIP','Lumpsum','Redemption')),
    amount_inr REAL,
    units REAL,
    kyc_status TEXT,
    payment_mode TEXT,
    annual_income_lakh REAL,
    gender TEXT,
    age_group REAL
);

CREATE TABLE fact_performance(
    perf_id INT PRIMARY KEY AUTOINCREMENT,
    fund_id INT REFERENCES dim_fund(fund_id),
    date_id INT REFERENCES dim_date(date_id),
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    expense_ratio_pct REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    risk_grade TEXT
);

CREATE TABLE fact_aum(
    aum_id INT PRIMARY KEY AUTOINCREMENT,
    fund_id INT REFERENCES dim_fund(fund_id),
    date_id INT REFERENCES dim_date(date_id),
    aum_crores REAL,
    nav REAL
);