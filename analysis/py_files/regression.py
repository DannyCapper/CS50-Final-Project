"""
This script runs a simple linear regression model of runs scored on wickets taken
"""

import json
import sqlite3
import statsmodels.api as sm
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    """
    Main function to perform linear regression on run_score and wicket_total data.
    """
    # Set the directory path for the database
    database_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/analysis/sql_database/cricket.db")

    # Connect to the SQL database and retrieve run_score and wicket_total data
    run_score, wicket_total = get_data_from_database(database_path)

    # Perform linear regression on the data and print the results
    results = perform_linear_regression(run_score, wicket_total)

    # Plot the regression model
    plot_regression(run_score, wicket_total, results)


def get_data_from_database(database_path: Path):
    """
    Connects to the SQL database and retrieves run_score and wicket_total data.

    Args:
        database_path: The path to the database.

    Returns:
        Two lists containing run_score and wicket_total data.
    """
    with sqlite3.connect(database_path) as conn:
        # Create a cursor
        c = conn.cursor()

        # Create two empty lists for storing data
        run_score = []
        wicket_total = []

        # Fetch all table names as a list of tuples
        tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

        # Loop over each table
        for table in tables:
            # Fetch table name
            table_name = table[0]

            # Append run_score to list
            c.execute(f"SELECT run_total FROM {table_name} WHERE ball = 1")
            run_score.append(c.fetchone()[0])

            # Append wicket_total to list
            c.execute(f"SELECT wicket_total FROM {table_name} WHERE ball = 1")
            wicket_total.append(c.fetchone()[0])

    return run_score, wicket_total

def perform_linear_regression(run_score, wicket_total):
    """
    Performs linear regression on the run_score and wicket_total data and prints the results.

    Args:
        run_score: List of run scores.
        wicket_total: List of wicket totals.
    """
    # Create a DataFrame from the two lists
    data = {"y": run_score, "x": wicket_total}
    df = pd.DataFrame(data)

    # Add a constant column to the DataFrame for the intercept
    df = sm.add_constant(df)

    # Fit the regression model
    model = sm.OLS(df['y'], df[['const', 'x']])
    results = model.fit()

    # Print the summary of the regression results
    print(results.summary())

    # Return results
    return results


def plot_regression(run_score, wicket_total, results):
    """
    Plots a scatter plot of the data points and the regression line.

    Args:
        run_score: List of run scores.
        wicket_total: List of wicket totals.
        results: Fitted linear regression model results.
    """
    # Create a DataFrame from the two lists
    data = {"y": run_score, "x": wicket_total}
    df = pd.DataFrame(data)

    # Create a scatter plot of the data points
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='x', y='y', alpha=0.5)

    # Plot the regression line
    x_values = df['x']
    y_values = results.params[0] + results.params[1] * x_values
    plt.plot(x_values, y_values, color='red', lw=2)

    # Set labels and title
    plt.xlabel('Wickets Lost')
    plt.ylabel('Run Score')
    plt.title('Linear Regression Model')

    # Set directory path for file to be saved
    output_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/website/static/regression.png")

    # Save the figure to a file
    plt.savefig(output_path)

if __name__ == "__main__":
    main()