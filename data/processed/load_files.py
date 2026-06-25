from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///bluestock_mf.db')

files = {
    'nav_history':'data/processed/clean_nav_history.csv',
    'investor_transactions': 'data/processed/clean_investor_transactions.csv',
    'schema_performance':'data/processed/clean_schema_performance.csv',
}

for table_name, path in files.items():
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    # Verifying row count
    db_count = pd.read_sql(f'SELECT COUNT(*) as cnt FROM {table_name}', engine)['cnt'][0]
    print(f"{table_name}: CSV={len(df)}, DB={db_count}, Match={len(df)==db_count}")
    print("Done!")