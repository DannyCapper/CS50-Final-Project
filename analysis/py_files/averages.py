import json
from pathlib import Path
from statistics import mean
import matplotlib.pyplot as plt


def main():
    """
    Main function to load data, calculate averages, and plot graph.
    """
    data_file_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/analysis/output/match_situation_tracker_v5.JSON")
    data = load_data(data_file_path)
    max_ball = max(int(situation.split("-")[2]) for situation in data.keys())
    ball_numbers, ball_averages = calculate_averages(data, max_ball)
    plot_graph(ball_numbers, ball_averages)


def load_data(file_path):
    """
    Load match data from a JSON file and return a dictionary.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: A dictionary containing match data.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def calculate_averages(data, max_ball):
    """
    Calculate the average wicket difference for each ball in the match.

    Args:
        data (dict): A dictionary containing match data.
        max_ball (int): The maximum ball number.

    Returns:
        tuple: A tuple containing two lists: ball numbers and their corresponding averages.
    """
    ball_averages = []
    for i in range(1, max_ball+1):
        ball_data = [data[situation][0] - data[situation][1] for situation in data.keys() if situation.split("-")[2] == str(i)]
        ball_average = mean(ball_data) if ball_data else None
        ball_averages.append(ball_average)
    ball_numbers = list(range(1, max_ball+1))
    return ball_numbers, ball_averages


def plot_graph(x_values, y_values):
    """
    Plot a line graph of y_values against x_values.

    Args:
        x_values (list): List of x values.
        y_values (list): List of y values.
    """
    plt.plot(x_values, y_values)
    plt.xlabel("Ball")
    plt.ylabel("Value of a wicket")
    plt.title("Value of a wicket over the course of a game")
    
    # Set directory path for file to be saved
    output_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/website/static/averages.png")

    # Save the figure to a file
    plt.savefig(output_path)


if __name__ == "__main__":
    main()
