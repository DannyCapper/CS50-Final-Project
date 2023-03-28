import os
import json
import sqlite3 

# Connect to the SQL database
database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "sql_database", "cricket.db")
conn = sqlite3.connect(database_path)

# Create a cursor
c = conn.cursor()

# Create an empty dictionary tracking match situation counts
match_situation_tracker = {}

#Fetch all table names as a list of tuples
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()

# Loop over each table
for table in tables:

    # Fetch all rows as a list of tuples
    c.execute("SELECT * FROM " + table[0])
    rows = c.fetchall()

    # Define match id variable
    match_id = table[0].split('_')[1]

    # Loop over each row
    for row in rows:

        # Define match situation and key variables
        match_situation = row[7]

        # Check if match situation already in dictionary
        if match_situation not in match_situation_tracker:
            
            # Add a new key-value pair to the dictionary. Key is match situation and value is a list containing the match situation
            list = []
            match_situation_tracker[match_situation] = list
        
        # Add match_id to list
        match_situation_tracker[match_situation].append(match_id)

# Open the text file and read the contents into a dictionary
output_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker.txt")
with open(output_path, "w") as f:
    json.dump(match_situation_tracker, f)

# Close the cursor and the database connection
c.close()
conn.close()