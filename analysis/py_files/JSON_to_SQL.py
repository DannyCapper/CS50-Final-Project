import json
import os
import sqlite3 

# Connect to the SQL database
database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "sql_database", "cricket.db")
conn = sqlite3.connect(database_path)

# Create a cursor
c = conn.cursor()

# Set the directory path
dir_path = '/mnt/c/WINDOWS/system32/CS50-Final-Project/data/T20I_male'

# Loop through all the files in the directory
for filename in os.listdir(dir_path):

    # Open the JSON file
    with open(os.path.join(dir_path, filename)) as f:

        # Read the contents of the file
        file_contents = f.read()

        # Check if the file is empty
        if not file_contents:
                print(f"Error: {filename} is empty.")
                continue
        
        try:
            # Try to parse the JSON data
            data = json.loads(file_contents)

            # Assign SQL table name
            table_name = f"match_{filename.split('.')[0]}"

            # Create SQL table for that match
            c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ball INTEGER PRIMARY KEY, over INTEGER NOT NULL, cum_runs INTEGER NOT NULL, run_total INTEGER, cum_wickets INTEGER NOT NULL, wicket_total INTEGER, runs INTEGER NOT NULL, wicket INTEGER NOT NULL, match_situation TEXT NOT NULL, bowler TEXT NOT NULL)")

            # Create tracker variables for ball, wickets, and runs
            ball = 1
            cum_runs = 0
            run_total = 0
            wicket_total = 0
            cum_wickets = 0
            match_situation = "0-0-1"

            # Count the number of overs
            overs = len(data["innings"][0]["overs"])

            # Loop over every over
            for i in range(overs):

                # Loop over every delivery in each over
                deliveries = len(data["innings"][0]["overs"][i]["deliveries"])
                for j in range(deliveries):

                    # Extract runs scored for that ball
                    runs = data["innings"][0]["overs"][i]["deliveries"][j]["runs"]["total"]
            
                    # Extract if a wicket was taken that ball
                    try:
                        check_for_wicket = data["innings"][0]["overs"][i]["deliveries"][j]["wickets"]
                        wicket = 1
                    except KeyError:
                        wicket = 0

                    # Extract bowler name for that ball
                    bowler = data["innings"][0]["overs"][i]["deliveries"][j]["bowler"]

                    # Insert SQL row
                    c.execute(f"INSERT OR IGNORE INTO {table_name} (ball, over, cum_runs, cum_wickets, runs, wicket, match_situation, bowler) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ball, i + 1, cum_runs, cum_wickets, runs, wicket, match_situation, bowler))

                    # Update ball, cum_runs, cum_wickets and match_situation values
                    ball += 1
                    cum_runs += runs
                    run_total += cum_runs
                    cum_wickets += wicket
                    wicket_total += cum_wickets
                    match_situation = "{}-{}-{}".format(cum_runs, cum_wickets, ball)

                    # Update run_total and wicket_total columns
                    c.execute(f"UPDATE {table_name} SET run_total = ?", (cum_runs,))
                    c.execute(f"UPDATE {table_name} SET wicket_total = ?", (cum_wickets,))
            
        except json.decoder.JSONDecodeError as e:
            
            # Handle the JSON decoding error
            print(f"Error: {filename} contains invalid JSON data. {e}")

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
c.close()
conn.close()