# Data Dictionary — Bluestock MF

## dim_fund
| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| fund_id | INTEGER | Unique identifier for each fund | Generated |
| amfi_code | INT | Official AMFI code assigned to each mutual fund schema in India | clean_nav_history.csv |
| schema_name | TEXT | Full name of the mutual fund schema | clean_schema_performance.csv |
| fund_house | TEXT | Asset Management Company managing the fund e.g. SBI MF, HDFC MF | clean_schema_performance.csv |
| category | TEXT | Fund category e.g. Equity, Debt, Hybrid | clean_schema_performance.csv |
| plan | TEXT | Direct or Regular plan | clean_schema_performance.csv |

## dim_date
| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| date_id | INTEGER | Unique identifier for each date | Generated |
| date | DATE | Calendar date | clean_nav_history.csv |

## fact_nav
| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| nav_id | INTEGER | Unique identifier for each NAV record | Generated |
| fund_id | INT | FK to dim_fund | clean_nav_history.csv |
| date_id | INT | FK to dim_date | clean_nav_history.csv |
| nav | REAL | Net Asset Value in INR — price of one unit of the fund on that date | clean_nav_history.csv |

## fact_transactions
| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| txn_id | INTEGER | Unique identifier for each transaction | Generated |
| amfi_code | INT | AMFI code of the fund being transacted | clean_investor_transactions.csv |
| investor_id | TEXT | Unique identifier for each investor | clean_investor_transactions.csv |
| fund_id | INT | FK to dim_fund | clean_investor_transactions.csv |
| date_id | INT | FK to dim_date | clean_investor_transactions.csv |
| transaction_date | DATE | Date the transaction was made | clean_investor_transactions.csv |
| transaction_type | TEXT | Type of transaction — SIP, Lumpsum, or Redemption | clean_investor_transactions.csv |
| amount_inr | REAL | Transaction amount in Indian Rupees | clean_investor_transactions.csv |
| units | REAL | Number of fund units bought or sold | clean_investor_transactions.csv |
| kyc_status | TEXT | KYC verification status of the investor | clean_investor_transactions.csv |
| payment_mode | TEXT | Mode of payment e.g. UPI, Net Banking | clean_investor_transactions.csv |
| annual_income_lakh | REAL | Investor's annual income in Lakhs | clean_investor_transactions.csv |
| gender | TEXT | Gender of the investor | clean_investor_transactions.csv |
| age_group | TEXT | Age group of the investor e.g. 25-34 | clean_investor_transactions.csv |

## fact_performance
| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| perf_id | INTEGER | Unique identifier for each performance record | Generated |
| fund_id | INT | FK to dim_fund | clean_schema_performance.csv |
| date_id | INT | FK to dim_date | clean_schema_performance.csv |
| return_1yr_pct | REAL | Percentage return over 1 year | clean_schema_performance.csv |
| return_3yr_pct | REAL | Percentage return over 3 years | clean_schema_performance.csv |
| return_5yr_pct | REAL | Percentage return over 5 years | clean_schema_performance.csv |
| expense_ratio_pct | REAL | Annual fee charged by the fund as % of AUM | clean_schema_performance.csv |
| sharpe_ratio | REAL | Return per unit of total risk — higher is better | clean_schema_performance.csv |
| sortino_ratio | REAL | Return per unit of downside risk only — higher is better | clean_schema_performance.csv |
| risk_grade | TEXT | Risk level of the fund e.g. Low, Moderate, High | clean_schema_performance.csv |

## fact_aum
| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| aum_id | INTEGER | Unique identifier for each AUM record | Generated |
| fund_id | INT | FK to dim_fund | clean_schema_performance.csv |
| date_id | INT | FK to dim_date | clean_schema_performance.csv |
| aum_crores | REAL | Total Assets Under Management in Indian Crores | clean_schema_performance.csv |
| nav | REAL | Net Asset Value at the time of AUM recording | clean_nav_history.csv |