import pandas as pd
import mysql.connector
from db_config import db_config

#  Connect to MySQL
print("Fetching data from database...")
conn = mysql.connector.connect(**db_config)

# Read SQL directly into a Pandas DataFrame 
query = "SELECT * FROM jobs"
df = pd.read_sql(query, conn)
conn.close()

print(f"Total rows fetched: {len(df)}")

# Data Cleaning 

df['is_senior'] = df['title'].str.contains('Senior|Sr.|Lead', case=False, regex=True)

# Analysis
print("\n--- Job Market Insights ---")
print(f"Total Jobs Found: {len(df)}")
print(f"Senior Roles: {df['is_senior'].sum()}")
print("Top 5 Companies hiring:")
print(df['company'].value_counts().head(5))

# Export to CSV 
output_file = "daily_job_report.csv"
df.to_csv(output_file, index=False)
print(f"\nReport generated successfully: {output_file}")