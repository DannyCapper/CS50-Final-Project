"""
This script process a JSON file which tracks the frequency of match situations in the database (where n > 1 for each sub-group i.e. wicket next ball & no wicket next ball), and outputs a JSON file tracking the frequency of match situations divided by sub-group
"""

import json
import sqlite3
from pathlib import Path


def main():
    """
    Main function to process the cricket database and create a match situation tracker with subgroups.
    """
    # Set the directory path for the database and input/output files
    database_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/sql_database/cricket.db"
    )
    input_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v3.JSON"
    )
    output_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v4.JSON"
    )

    # Load the match situation tracker from the input file
    match_situation_tracker_v3 = load_match_situation_tracker(input_path)

    # Connect to the database and create a cursor
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        # Create subgroups for match situations based on wickets taken in the next ball
        match_situation_tracker_v4 = create_subgroups(
            cursor, match_situation_tracker_v3
        )

    # Save the match situation tracker with subgroups to the output file
    save_match_situation_tracker(match_situation_tracker_v4, output_path)


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


def create_subgroups(cursor, match_situation_tracker):
    """
    Create subgroups for match situations based on wickets taken in the next ball.

    Args:
        cursor: The SQLite cursor object.
        match_situation_tracker: The dictionary containing match situations.

    Returns:
        A dictionary containing match situations with subgroups.
    """
    subgroups = {}

    # Loop over each match situation
    for situation in match_situation_tracker.keys():
        list1 = []
        list2 = []

        matches = len(match_situation_tracker[situation])
        ball = situation.split("-")[2]

        # Loop over each match in the list
        for match_id in match_situation_tracker[situation]:
            table_name = "match_" + match_id

            # Check if wicket taken next ball
            cursor.execute(f"SELECT wicket FROM {table_name} WHERE ball = ?", (ball,))
            n = cursor.fetchone()[0]

            # Append to appropriate list
            if n == 0:
                list1.append(match_id)
            else:
                list2.append(match_id)

        # Create meta-list and assign to relevant key in the dictionary
        meta_list = [list1, list2]
        subgroups[situation] = meta_list

    return subgroups


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
