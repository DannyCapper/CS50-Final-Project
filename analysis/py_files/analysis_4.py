import os
import json
import sqlite3 

# Connect to the SQL database
database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "sql_database", "cricket.db")
conn = sqlite3.connect(database_path)

# Create a cursor
c = conn.cursor()

# Open the file for reading
input_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v3.txt")
with open(input_path, "r") as f:
    # Load the contents of the file as a string and convert it to a dictionary
    match_situation_tracker_v3 = json.load(f)

# Create empty dictionary for storing match situations where n > 1 for both sub_groups
match_situation_tracker_v4 = {}

# Loop over each match situation
for situation in match_situation_tracker_v3.keys():

    # Create empty lists
    list1 = []
    list2 = []

    # Create tracker variables
    matches = len(match_situation_tracker_v3[situation])
    ball = situation.split('-')[2]

    # Loop over each match in the list
    for i in range(matches):

        # Define table name and match_id
        table_name = "match_" + match_situation_tracker_v3[situation][i]
        match_id = match_situation_tracker_v3[situation][i]

        # Check if wicket taken next ball
        c.execute(f"SELECT wicket FROM {table_name} WHERE ball = ?", (ball,))
        n = c.fetchone()[0]

        # Append to appropriate list
        if n == 0:
            list1.append(match_id)
        else:
            list2.append(match_id)
    
    # Create meta-list and assign to relevant key in the dictionary
    meta_list = [list1, list2]
    match_situation_tracker_v4[situation] = meta_list

# Open the text file and read the contents into a dictionary
output_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v4.txt")
with open(output_path, "w") as f:
    json.dump(match_situation_tracker_v4, f)

# Close the cursor and the database connection
c.close()
conn.close()