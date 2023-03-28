import os
import json
import sqlite3
import statsmodels.api as sm
import pandas as pd

# Connect to the SQL database
database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "sql_database", "cricket.db")
conn = sqlite3.connect(database_path)

# Create a cursor
c = conn.cursor()

# Create two empty lists for storing data
run_score = []
wicket_total = []

#Fetch all table names as a list of tuples
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()

# Loop over each table
for table in tables:

    # Fetch table name
    table_name = table[0]

    # Append run_score to list
    c.execute(f"SELECT run_total FROM {table_name} WHERE ball = 1")
    run_score.append(c.fetchone()[0])

    # Append wicket_total to list
    c.execute(f"SELECT wicket_total FROM {table_name} WHERE ball = 1")
    wicket_total.append(c.fetchone()[0])

# Close the cursor and the database connection
c.close()
conn.close()

# Create a DataFrame from the two lists
data = {"y": run_score, "x": wicket_total}
df = pd.DataFrame(data)

# Add a constant column to the DataFrame for the intercept
df = sm.add_constant(df)

# Fit the regression model
model = sm.OLS(df['y'], df[['const', 'x']])
results = model.fit()

# Print the summary of the regression results
print(results.summary())
