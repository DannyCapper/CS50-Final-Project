import os
import json
import sqlite3 

# Connect to the SQL database
database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "sql_database", "cricket.db")
conn = sqlite3.connect(database_path)

# Create a cursor
c = conn.cursor()

# Open the file for reading
input_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v2.txt")
with open(input_path, "r") as f:
    # Load the contents of the file as a string and convert it to a dictionary
    match_situation_tracker_v2 = json.load(f)

# Create empty dictionary for storing match situations where n > 1 for both sub_groups
match_situation_tracker_v3 = {}

# Loop over each match situation
for situation in match_situation_tracker_v2.keys():

    # Set-up counter variables and ball variable
    matches = len(match_situation_tracker_v2[situation])
    wicket_next_ball = 0
    ball = situation.split('-')[2]

    # Loop over each match in the list
    for i in range(matches):

        # Define table name
        table_name = "match_" + match_situation_tracker_v2[situation][i]

        # Check if wicket taken next ball
        c.execute(f"SELECT wicket FROM {table_name} WHERE ball = ?", (ball,))
        n = c.fetchone()[0]
        if n == 1:

            # Add 1 to wicket_next_ball counter
            wicket_next_ball += 1

    # Add situation to tracker if wicket_next_ball and no_wicket_next_ball > 0
    no_wicket_next_ball = matches - wicket_next_ball
    if wicket_next_ball > 0 and no_wicket_next_ball > 0:
        match_situation_tracker_v3[situation] = match_situation_tracker_v2[situation]

# Open the text file and read the contents into a dictionary
output_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v3.txt")
with open(output_path, "w") as f:
    json.dump(match_situation_tracker_v3, f)

# Close the cursor and the database connection
c.close()
conn.close()