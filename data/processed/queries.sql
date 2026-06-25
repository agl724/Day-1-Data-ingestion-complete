--1 Fetching alll the rows and columns from every table

SELECT * FROM dim_fund;
SELECT * FROM dim_date;
SELECT * FROM fact_nav;
SELECT * FROM fact_transactions;
SELECT * FROM fact_performance;
SELECT * FROM fact_aum;

--2  . All funds with their basic info
SELECT amfi_code, schema_name, fund_house, category, plan
FROM dim_fund;

--3 Top 10 largest funds by aum
 
SELECT a.aum_id, f.schema_name, a.aum_crores, f.fund_house, f.plan
FROM fact_aum a
JOIN dim_fund f
ON a.fund_id = f.fund_id
ORDER BY aum_crores DESC
LIMIT 10;

--4 Average NAV per month
SELECT AVG(f.nav) as avg_nav, df.schema_name, date_id
FROM fact_nav f
JOIN dim_date d
ON f.date_id = d.date_id
JOIN dim_fund df
ON f.fund_id = df.fund_id
GROUP BY df.schema_name;

--5 Transactions by date and gender --
SELECT txn_id, investor_id, transaction_date, gender
FROM fact_transactions
ORDER BY transaction_date, gender;

--6 Funds with expenses ratio < 1%--
SELECT p.perf_id, f.fund_id, p.expense_ratio_pct
FROM fact_performance p
INNER JOIN dim_fund f
ON p.fund_id = f.fund_id
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct;

--7 Best performing funds by 3yr returns
SELECT f.fund_id, MAX(p.return_3yr_pct) AS best_3yr_returns, f.schema_name
FROM fact_performance p
JOIN dim_fund f
ON p.fund_id = f.fund_id
GROUP BY f.fund_id, f.schema_name
ORDER BY best_3yr_returns DESC
LIMIT 15;

--8 Category-wise average expense ratio
SELECT f.category, ROUND(AVG(p.expense_ratio_pct), 3) AS avg_expense_ratio
FROM fact_performance p 
JOIN dim_fund f ON p.fund_id = f.fund_id
GROUP BY f.category 
ORDER BY avg_expense_ratio;

--9 best performing funds in 1yr, 3yr, and 5 yr reutrns
SELECT f.amfi_code, f.schema_name, f.fund_house, f.category, return_1yr_pct, return_3yr_pct, return_5yr_pct,
RANK() OVER( ORDER BY return_1yr_pct DESC) AS rank_1yr,
RANK() OVER( ORDER BY return_3yr_pct DESC) AS rank_3yr,
RANK() OVER( ORDER BY return_5yr_pct DESC) AS rank_5yr
FROM fact_performance p
JOIN dim_fund f
ON p.fund_id = f.fund_id
ORDER BY return_5yr_pct DESC;


--10 Funds with low risk grade
SELECT risk_grade, perf_id, schema_name, f.fund_id, fund_house, return_1yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.fund_id = f.fund_id
WHERE p.risk_grade = 'LOW'
ORDER BY return_1yr_pct DESC;
