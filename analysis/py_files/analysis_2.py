import os
import json

# Open the file for reading
input_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker.txt")
with open(input_path, "r") as f:
    # Load the contents of the file as a string and convert it to a dictionary
    match_situation_tracker = json.load(f)

# Create empty dictionary for storing match situations where n > 1
match_situation_tracker_v2 = {}

# Loop over each match situation
for situation in match_situation_tracker.keys():

    # Eliminate those where n < 2
    if len(match_situation_tracker[situation]) > 1:
        match_situation_tracker_v2[situation] = match_situation_tracker[situation]

# Open the text file and read the contents into a dictionary
output_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v2.txt")
with open(output_path, "w") as f:
    json.dump(match_situation_tracker_v2, f)