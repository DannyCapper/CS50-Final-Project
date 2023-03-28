import os
import json

# Open the file for reading
input_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v5.txt")
with open(input_path, "r") as f:
    # Load the contents of the file as a string and convert it to a dictionary
    match_situation_tracker_v5 = json.load(f)

# Calculate total frequency for weightings
total_frequency = 0
for situation in match_situation_tracker_v5.keys():
    total_frequency += match_situation_tracker_v5[situation][2]

# Create tracker for weighted average
weighted_average = 0

# Loop over each match situation
for situation in match_situation_tracker_v5.keys():

    # Calculate difference of averages
    difference = match_situation_tracker_v5[situation][0] - match_situation_tracker_v5[situation][1]

    # Calculate weight
    frequency = match_situation_tracker_v5[situation][2]
    weight = frequency / total_frequency

    # Multiply difference by weight
    diff_weight = difference * weight

    # Add to weighted average
    weighted_average += diff_weight

# Define "final answer"
wicket_value = weighted_average - 1
weighted_average = round(wicket_value, 1)

# Print out weighted average
print(f"Weighted average is: {weighted_average}")