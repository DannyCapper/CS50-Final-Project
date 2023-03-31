"""
This script processes a JSON file tracking match situations data and calculates the simple average wicket value
"""

import json
from pathlib import Path


def main():
    """
    Main function to calculate the simple average wicket value using the match situation tracker.
    """
    # Set the directory path for the input file
    input_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v5.JSON"
    )

    # Load the match situation tracker from the input file
    match_situation_tracker_v5 = load_match_situation_tracker(input_path)

    # Calculate the simple average wicket value
    simple_average = calculate_simple_average(match_situation_tracker_v5)

    # Print the simple average wicket value
    print(f"Simple average is: {simple_average}")


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


def calculate_simple_average(match_situation_tracker):
    """
    Calculate the simple average wicket value using the match situation tracker.

    Args:
        match_situation_tracker: The dictionary containing match situations.

    Returns:
        A float representing the simple average wicket value.
    """
    length = len(match_situation_tracker)
    counter = 0

    # Loop over each match situation
    for situation in match_situation_tracker.keys():
        counter += (
            match_situation_tracker[situation][0]
            - match_situation_tracker[situation][1]
        )

    wicket_value = counter / (length - 1)
    return round(wicket_value, 1)


if __name__ == "__main__":
    main()
