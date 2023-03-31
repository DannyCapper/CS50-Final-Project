"""
This script processes an SQLite database and outputs a JSON file tracking the number of times a match situation arises
"""

import json
import sqlite3
from pathlib import Path

# Set the directory path for the database and output file
database_path = Path(
    "/mnt/c/USERS/danny/CS50-Final-Project/analysis/sql_database/cricket.db"
)
output_path = Path(
    "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker.JSON"
)


def main():
    """
    Main function to process the cricket database and create a match situation tracker.
    """
    match_situation_tracker = {}

    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        tables = get_all_tables(cursor)

        for table in tables:
            process_table(cursor, table, match_situation_tracker)

    save_match_situation_tracker(match_situation_tracker, output_path)


def get_all_tables(cursor):
    """
    Get all table names in the database.

    Args:
        cursor: The SQLite cursor object.

    Returns:
        A list of table names.
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [table[0] for table in cursor.fetchall()]


def process_table(cursor, table, match_situation_tracker):
    """
    Process a table to extract match situations and update the match_situation_tracker dictionary.

    Args:
        cursor: The SQLite cursor object.
        table: The name of the table to process.
        match_situation_tracker: The dictionary to update with match situations.
    """
    rows = cursor.execute(f"SELECT * FROM {table}").fetchall()
    match_id = table.split("_")[1]

    for row in rows:
        match_situation = row[8]

        if match_situation not in match_situation_tracker:
            match_situation_tracker[match_situation] = []

        match_situation_tracker[match_situation].append(match_id)


def save_match_situation_tracker(match_situation_tracker, output_path):
    """
    Save the match situation tracker dictionary as a JSON file.

    Args:
        match_situation_tracker: The dictionary containing match situations.
        output_path: The path to save the JSON file.
    """
    with open(output_path, "w") as f:
        json.dump(match_situation_tracker, f)


if __name__ == "__main__":
    main()
