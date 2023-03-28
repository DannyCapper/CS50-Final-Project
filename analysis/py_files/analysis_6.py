import os
import json

# Open the file for reading
input_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/analysis", "txt_files", "match_situation_tracker_v5.txt")
with open(input_path, "r") as f:
    # Load the contents of the file as a string and convert it to a dictionary
    match_situation_tracker_v5 = json.load(f)

# Calculate length of dictionary
length = len(match_situation_tracker_v5)

# Define counter variable
counter = 0

# Loop over each match situation
for situation in match_situation_tracker_v5.keys():
    counter += match_situation_tracker_v5[situation][0] - match_situation_tracker_v5[situation][1]

# Define "final answer"
wicket_value = counter / length - 1
simple_average = round(wicket_value, 1)

print(f"Simple average is: {simple_average}")