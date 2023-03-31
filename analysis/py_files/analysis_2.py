"""
This script processes a JSON file which tracks the frequency of match situations in the database and eliminates match situations where the sample size is 1
"""

import json
from pathlib import Path


def main():
    # Set the directory path for the input and output files
    input_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker.JSON"
    )
    output_path = Path(
        "/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v2.JSON"
    )

    match_situation_tracker = load_match_situation_tracker(input_path)
    match_situation_tracker_v2 = filter_match_situations(match_situation_tracker)
    save_match_situation_tracker(match_situation_tracker_v2, output_path)


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


def filter_match_situations(match_situation_tracker):
    """
    Filter match situations where the count is greater than 1.

    Args:
        match_situation_tracker: The dictionary containing match situations.

    Returns:
        A dictionary containing filtered match situations.
    """
    return {
        situation: match_list
        for situation, match_list in match_situation_tracker.items()
        if len(match_list) > 1
    }


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
