"""
This script processes a JSON file which tracks the frequency of match situations in the database (where n > 1) and eliminates match situations where there is not a sample size of at least 1 for each sub-group (i.e. wicket next ball & no wicket next ball)
"""

import json
import sqlite3
from pathlib import Path


def main():
    """
    Main function to process the cricket database and create a filtered match situation tracker.
    """
    # Set the directory path for the database and input/output files
    database_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/sql_database/cricket.db"
    )
    input_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v2.JSON"
    )
    output_path = Path(
        "/mnt/c/Users/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v3.JSON"
    )

    # Load the match situation tracker from the input file
    match_situation_tracker_v2 = load_match_situation_tracker(input_path)

    # Connect to the database and create a cursor
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        # Filter match situations based on the occurrence of wickets in the next ball
        match_situation_tracker_v3 = filter_match_situations(
            cursor, match_situation_tracker_v2
        )

    # Save the filtered match situation tracker to the output file
    save_match_situation_tracker(match_situation_tracker_v3, output_path)


def load_match_situation_tracker(input_path):
    """
    Load the match situation tracker from a JSON file.

    Args:
        input_path: The path to the input JSON file.

    Returns:
        A dictionary containing the match situations.
    """
    with open(input_path, "r") as f:
        return json.load(f)


def filter_match_situations(cursor, match_situation_tracker):
    """
    Filter match situations based on the occurrence of wickets in the next ball.

    Args:
        cursor: The SQLite cursor object.
        match_situation_tracker: The dictionary containing match situations.

    Returns:
        A dictionary containing filtered match situations.
    """
    filtered_situations = {}

    # Loop over each match situation
    for situation in match_situation_tracker.keys():
        matches = len(match_situation_tracker[situation])
        wicket_next_ball = 0
        ball = situation.split("-")[2]

        # Loop over each match in the list
        for match_id in match_situation_tracker[situation]:
            table_name = "match_" + match_id

            # Check if wicket taken next ball
            cursor.execute(f"SELECT wicket FROM {table_name} WHERE ball = ?", (ball,))
            n = cursor.fetchone()[0]

            if n == 1:
                wicket_next_ball += 1

        no_wicket_next_ball = matches - wicket_next_ball

        # Add situation to tracker if wicket_next_ball and no_wicket_next_ball > 0
        if wicket_next_ball > 0 and no_wicket_next_ball > 0:
            filtered_situations[situation] = match_situation_tracker[situation]

    return filtered_situations


def save_match_situation_tracker(match_situation_tracker, output_path):
    """
    Save the match situation tracker as a JSON file.

    Args:
        match_situation_tracker: The dictionary containing match situations.
        output_path: The path to save the JSON file.
    """
    with open(output_path, "w") as f:
        json.dump(match_situation_tracker, f)


if __name__ == "__main__":
    main()
