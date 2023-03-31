"""
This script processes a JSON file tracking the frequency of match situations divided by sub-group and calculates the average final runs for each sub-group
"""

import json
import sqlite3
from pathlib import Path


def main():
    """
    Main function to process the cricket database and create a match situation tracker with averages and frequency.
    """
    # Set the directory path for the database and input/output files
    database_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/sql_database/cricket.db"
    )
    input_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v4.JSON"
    )
    output_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v5.JSON"
    )

    # Load the match situation tracker from the input file
    match_situation_tracker_v4 = load_match_situation_tracker(input_path)

    # Connect to the database and create a cursor
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        # Calculate and store averages and frequency for each match situation
        match_situation_tracker_v5 = calculate_averages_and_frequency(
            cursor, match_situation_tracker_v4
        )

    # Save the match situation tracker with averages and frequency to the output file
    save_match_situation_tracker(match_situation_tracker_v5, output_path)


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


def calculate_averages_and_frequency(cursor, match_situation_tracker):
    """
    Calculate and store averages and frequency for each match situation.

    Args:
        cursor: The SQLite cursor object.
        match_situation_tracker: The dictionary containing match situations.

    Returns:
        A dictionary containing match situations with averages and frequency.
    """
    averages_and_frequency = {}

    # Loop over each match situation
    for situation in match_situation_tracker.keys():
        averages_list = []
        frequency = 0

        # Loop over each of the 2 lists
        for i in range(2):
            length = len(match_situation_tracker[situation][i])
            frequency += length
            sum_run_total = 0

            # Loop over each match in the list
            for match_id in match_situation_tracker[situation][i]:
                table_name = "match_" + match_id

                # Query the final run score and add to counter
                cursor.execute(f"SELECT run_total FROM {table_name} WHERE ball = 1")
                n = cursor.fetchone()[0]
                sum_run_total += n

            # Calculate average and store in list
            average_run_total = sum_run_total / length
            averages_list.append(average_run_total)

        # Append frequency to list
        averages_list.append(frequency)

        # Store list in dictionary
        averages_and_frequency[situation] = averages_list

    return averages_and_frequency


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
