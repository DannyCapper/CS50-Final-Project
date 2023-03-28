import os
import json
import sqlite3 

# Connect to the SQL database
database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "sql_database", "cricket.db")
conn = sqlite3.connect(database_path)

# Create a cursor
c = conn.cursor()

# Open the file for reading
input_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v4.txt")
with open(input_path, "r") as f:
    # Load the contents of the file as a string and convert it to a dictionary
    match_situation_tracker_v4 = json.load(f)

# Create empty dictionary for storing averages
match_situation_tracker_v5 = {}

# Loop over each match situation
for situation in match_situation_tracker_v4.keys():

    # Create a list for storing averages & frequency to be added to dictionary
    averages_list = []

    # Create a variable for tracking frequency
    frequency = 0

    # Loop over each of the 2 lists
    for i in range(2):

        # Calculate length of the list
        length = len(match_situation_tracker_v4[situation][i])
        frequency += length

        # Define counter variable
        sum_run_total = 0

        # Loop over each match in the list
        for j in range(length):

            # Lay out the table name
            table_name = "match_" + match_situation_tracker_v4[situation][i][j]

            # Query the final run score and add to counter
            c.execute(f"SELECT run_total FROM {table_name} WHERE ball = 1")
            n = c.fetchone()[0]
            sum_run_total += n

        # Calculate average and store in list
        average_run_total = sum_run_total / length
        averages_list.append(average_run_total)

    # Append frequency to list
    averages_list.append(frequency)

    # Store list in dictionary
    match_situation_tracker_v5[situation] = averages_list

# Open the text file and read the contents into a dictionary
output_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v5.txt")
with open(output_path, "w") as f:
    json.dump(match_situation_tracker_v5, f)

# Close the cursor and the database connection
c.close()
conn.close()