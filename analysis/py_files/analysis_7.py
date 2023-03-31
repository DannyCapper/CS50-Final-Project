"""
This script processes a JSON file tracking match situations data and calculates the weighted average wicket value
"""

import json
import os
from typing import Dict


def main():
    """
    Main function to calculate the weighted average wicket value using the match situation tracker.
    """
    input_path = os.path.join(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis",
        "output",
        "match_situation_tracker_v5.JSON",
    )

    # Load the match situation tracker from the input file
    match_situation_tracker_v5 = load_match_situation_tracker(input_path)

    # Calculate the weighted average wicket value
    weighted_average = calculate_weighted_average(match_situation_tracker_v5)

    # Print the weighted average wicket value
    print(f"Weighted average is: {weighted_average}")


def load_match_situation_tracker(input_path: str) -> Dict:
    """
    Load the match situation tracker from a JSON file.

    Args:
        input_path: The path to the input JSON file.

    Returns:
        A dictionary containing the match situations.
    """
    with open(input_path, "r") as f:
        return json.load(f)


def calculate_weighted_average(match_situation_tracker: Dict) -> float:
    """
    Calculate the weighted average wicket value using the match situation tracker.

    Args:
        match_situation_tracker: The dictionary containing match situations.

    Returns:
        A float representing the weighted average wicket value.
    """
    total_frequency = sum(
        match_situation_tracker[situation][2]
        for situation in match_situation_tracker.keys()
    )
    weighted_average = sum(
        (match_situation_tracker[situation][0] - match_situation_tracker[situation][1])
        * (match_situation_tracker[situation][2] / total_frequency)
        for situation in match_situation_tracker.keys()
    )

    wicket_value = weighted_average - 1
    return round(wicket_value, 1)


if __name__ == "__main__":
    main()
