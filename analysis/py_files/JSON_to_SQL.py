"""
This script processes JSON files containing cricket match data and inserts them into an SQLite database.
"""

import json
import sqlite3
from pathlib import Path

def main():
    """
    The main function connects to the SQLite database and loops through the JSON files.
    It calls the process_file function for each file.
    """
    # Set the directory path for the data
    dir_path = Path('/mnt/c/USERS/danny/CS50-Final-Project/data/T20I_male')

    # Set the directory path for the database
    database_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/analysis/sql_database/cricket.db")

    with sqlite3.connect(database_path) as conn:

        # Create a cursor
        c = conn.cursor()

        # Loop through all the files in the directory
        for file_path in dir_path.iterdir():

            # Call process_file function
            process_file(c, file_path)

def process_file(c, file_path):
    """
    This function processes a single JSON file, creating a new table in the SQLite database
    and inserting the match data into the table.

    Args:
        c (sqlite3.Cursor): The SQLite cursor object.
        file_path (Path): The file path of the JSON file.
    """
    # Open the JSON file
    with open(file_path) as f:

        # Read the contents of the file
        file_contents = f.read()
        
        # Parse the JSON data
        data = json.loads(file_contents)

        # Assign SQL table name
        table_name = f"match_{file_path.stem}"

        # Create SQL table for that match
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                ball INTEGER PRIMARY KEY,
                over INTEGER NOT NULL,
                cum_runs INTEGER NOT NULL,
                run_total INTEGER,
                cum_wickets INTEGER NOT NULL,
                wicket_total INTEGER,
                runs INTEGER NOT NULL,
                wicket INTEGER NOT NULL,
                match_situation TEXT NOT NULL,
                bowler TEXT NOT NULL
            )
        """)

        # Create tracker variables for ball, wickets, and runs
        ball = 1
        cum_runs = 0
        run_total = 0
        wicket_total = 0
        cum_wickets = 0
        match_situation = "0-0-1"

        # Loop over every over
        for i, over in enumerate(data["innings"][0]["overs"]):
            
            # Loop over every delivery in the over
            for j, delivery in enumerate(over["deliveries"]):

                # Extract runs scored for that ball
                runs = data["innings"][0]["overs"][i]["deliveries"][j]["runs"]["total"]
        
                # Extract if a wicket was taken that ball
                check_for_wicket = data["innings"][0]["overs"][i]["deliveries"][j].get("wickets")
                wicket = 1 if check_for_wicket else 0

                # Extract bowler name for that ball
                bowler = data["innings"][0]["overs"][i]["deliveries"][j]["bowler"]

                # Insert SQL row
                c.execute(f"""
                    INSERT INTO {table_name} (
                        ball, over, cum_runs, cum_wickets,
                        runs, wicket, match_situation, bowler
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (ball, i + 1, cum_runs, cum_wickets, runs, wicket, match_situation, bowler))

                # Update ball, cum_runs, cum_wickets and match_situation values
                ball += 1
                cum_runs += runs
                run_total += cum_runs
                cum_wickets += wicket
                wicket_total += cum_wickets
                match_situation = f"{cum_runs}-{cum_wickets}-{ball}"

                # Update run_total and wicket_total columns
                c.execute(f"UPDATE {table_name} SET run_total = ?, wicket_total = ?", (cum_runs, cum_wickets))

if __name__ == "__main__":
    main()