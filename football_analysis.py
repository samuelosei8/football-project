import sqlite3
import pandas as pd
import os

# Step 0: Define the CSV path
csv_path = os.path.join("data", "matches.csv")

# Step 1: Check if CSV exists
if not os.path.exists(csv_path):
    print(f"Error: CSV file not found at {csv_path}")
    exit()

# Step 2: Load CSV
df = pd.read_csv(csv_path)
print("CSV loaded successfully!")

# Step 3: Create SQLite database
conn = sqlite3.connect("football.db")
print("SQLite database created!")

# Step 4: Write data to SQL
df.to_sql("matches", conn, if_exists="replace", index=False)
print("Data written to SQL!")

# Step 5: Run SQL query (total goals per team)
query = """
SELECT home_team AS team, SUM(home_goals) AS goals
FROM matches
GROUP BY home_team
UNION
SELECT away_team AS team, SUM(away_goals) AS goals
FROM matches
GROUP BY away_team
ORDER BY goals DESC;
"""
team_goals = pd.read_sql(query, conn)
print("SQL query executed!")

# Step 6: Export to Excel
team_goals.to_excel("team_goals.xlsx", index=False)
print("Exported results to team_goals.xlsx ✅")

# Step 7: Close database connection
conn.close()
