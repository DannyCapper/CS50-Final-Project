"""
This script processes JSON files containing cricket match data and inserts them into an SQLite database.
"""

import json
from pathlib import Path
import sqlite3


def main():
    db_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/bowlers/sql_database/bowlers.db"
    )
    data_dir = Path("/mnt/c/USERS/danny/CS50-Final-Project/data/T20I_male")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        create_table(cursor)

        for file_path in data_dir.glob("*.json"):
            process_json_file(file_path, cursor)

        calculate_bowler_metrics(cursor)
        conn.commit()


def create_table(cursor):
    """Create a SQL table called bowlers."""
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS bowlers (
        name TEXT NOT NULL PRIMARY KEY,
        overs INTEGER,
        runs INTEGER,
        wickets INTEGER,
        economy FLOAT,
        average FLOAT,
        prop_score FLOAT
    )
    """
    )


def process_json_file(file_path, cursor):
    """Process a JSON file and update the bowlers table."""
    with open(file_path) as f:
        data = json.load(f)

    overs_count = len(data["innings"][0]["overs"])

    for i in range(overs_count):
        bowler = data["innings"][0]["overs"][i]["deliveries"][0]["bowler"]
        update_bowler_stats(data, cursor, i, bowler)


def update_bowler_stats(data, cursor, i, bowler):
    """Update bowler stats for each over."""
    try:
        cursor.execute("SELECT overs FROM bowlers WHERE name = ?", (bowler,))
        new_overs = cursor.fetchone()[0] + 1
        cursor.execute(
            "UPDATE bowlers SET overs = ? WHERE name = ?", (new_overs, bowler)
        )
    except TypeError:
        cursor.execute(
            "INSERT INTO bowlers (name, overs, runs, wickets) VALUES (?, 1, 0, 0)",
            (bowler,),
        )

    deliveries = len(data["innings"][0]["overs"][i]["deliveries"])
    for j in range(deliveries):
        update_runs_wickets(data, cursor, i, j, bowler)


def update_runs_wickets(data, cursor, i, j, bowler):
    """Update bowler's run and wicket count for each ball."""
    cursor.execute("SELECT runs FROM bowlers WHERE name = ?", (bowler,))
    new_runs = (
        cursor.fetchone()[0]
        + data["innings"][0]["overs"][i]["deliveries"][j]["runs"]["total"]
    )
    cursor.execute("UPDATE bowlers SET runs = ? WHERE name = ?", (new_runs, bowler))

    cursor.execute("SELECT wickets FROM bowlers WHERE name = ?", (bowler,))
    try:
        check_for_wicket = data["innings"][0]["overs"][i]["deliveries"][j]["wickets"]
        wicket = 1
    except KeyError:
        wicket = 0

    new_wickets = cursor.fetchone()[0] + wicket
    cursor.execute(
        "UPDATE bowlers SET wickets = ? WHERE name = ?", (new_wickets, bowler)
    )


def calculate_bowler_metrics(cursor):
    """Calculate bowler's economy, average, and prop_score."""
    cursor.execute("SELECT * FROM bowlers")
    rows = cursor.fetchall()

    for row in rows:
        bowler = row[0]
        overs, runs, wickets = row[1], row[2], row[3]

        economy = round(runs / overs, 2)

        try:
            average = round(runs / wickets, 2)
        except ZeroDivisionError:
            average = 10000

        prop_score = economy

        cursor.execute(
            "UPDATE bowlers SET economy = ? WHERE name = ?", (economy, bowler)
        )
        cursor.execute(
            "UPDATE bowlers SET average = ? WHERE name = ?", (average, bowler)
        )
        cursor.execute(
            "UPDATE bowlers SET prop_score = ? WHERE name = ?", (prop_score, bowler)
        )


if __name__ == "__main__":
    main()
