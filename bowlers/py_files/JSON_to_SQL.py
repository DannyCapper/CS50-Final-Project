import json
import os
import sqlite3 

# Connect to the SQL database
database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/bowlers", "sql_database", "bowlers.db")
conn = sqlite3.connect(database_path)

# Create a cursor
c = conn.cursor()

# Add a SQL table called bowlers
c.execute("CREATE TABLE IF NOT EXISTS bowlers (name TEXT NOT NULL PRIMARY KEY, overs INTEGER, runs INTEGER, wickets INTEGER, economy FLOAT, average FLOAT, prop_score FLOAT)")

# Define directory for dataset
dir_path = '/mnt/c/WINDOWS/system32/CS50-Final-Project/data/T20I_male'

# Loop over each JSON file
for filename in os.listdir(dir_path):

    # Open the JSON file
    with open(os.path.join(dir_path, filename)) as f:

        # Read the contents of the file
        file_contents = f.read()

        # Parse the JSON data
        data = json.loads(file_contents)

        # Count the number of overs
        overs = len(data["innings"][0]["overs"])

        # Loop over every over
        for i in range(overs):

            # Add the bowler to our SQL table if not already in and update overs count
            bowler = data["innings"][0]["overs"][i]["deliveries"][0]["bowler"]

            try:
                c.execute("SELECT overs FROM bowlers WHERE name = ?", (bowler,))
                new_overs = c.fetchone()[0] + 1
                c.execute("UPDATE bowlers SET overs = ? WHERE name = ?", (new_overs, bowler))
            except TypeError:
                c.execute("INSERT INTO bowlers (name, overs, runs, wickets) VALUES (?, 1, 0, 0)", (bowler,))

            # Loop over each ball in the over
            deliveries = len(data["innings"][0]["overs"][i]["deliveries"])
            for j in range(deliveries):

                # Add to the  bowler's run count
                c.execute("SELECT runs FROM bowlers WHERE name = ?", (bowler,))
                new_runs = c.fetchone()[0] + data["innings"][0]["overs"][i]["deliveries"][j]["runs"]["total"]
                c.execute("UPDATE bowlers SET runs = ? WHERE name = ?", (new_runs, bowler))

                # Add to the bowler's wicket count
                c.execute("SELECT wickets FROM bowlers WHERE name = ?", (bowler,))

                # Extract if a wicket was taken that ball
                try:
                    check_for_wicket = data["innings"][0]["overs"][i]["deliveries"][j]["wickets"]
                    wicket = 1
                except KeyError:
                    wicket = 0

                new_wickets = c.fetchone()[0] + wicket

                c.execute("UPDATE bowlers SET wickets = ? WHERE name = ?", (new_wickets, bowler))

# Fetch all rows as a list of tuples
c.execute("SELECT * FROM bowlers")
rows = c.fetchall()

# Loop over each row
for row in rows:

    # Fetch bowler's name
    bowler = row[0]

    # Calculate a bowler's economy, average and prop_score
    overs, runs, wickets = row[1], row[2], row[3]

    economy = round(runs / overs, 2)

    try:
        average = round(runs / wickets, 2)
    except ZeroDivisionError:
        average = 10000

    prop_score = economy

    # Update these variables in the SQL table
    c.execute("UPDATE bowlers SET economy = ? WHERE name = ?", (economy, bowler))
    c.execute("UPDATE bowlers SET average = ? WHERE name = ?", (average, bowler))
    c.execute("UPDATE bowlers SET prop_score = ? WHERE name = ?", (prop_score, bowler))

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
c.close()
conn.close()