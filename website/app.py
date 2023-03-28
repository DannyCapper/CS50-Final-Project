from flask import Flask, flash, redirect, render_template, request, session
import os
import sqlite3

# Configure application
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/methodology')
def methodology():
    return render_template("methodology.html")


@app.route('/bowler_comparisons', methods=["GET", "POST"])
def bowler_comparisons():

    # Connect to the SQL database
    database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/bowlers", "sql_database", "bowlers.db")
    conn = sqlite3.connect(database_path)

    # Create a cursor
    c = conn.cursor()

    # Query the bowlers
    c.execute("SELECT name FROM bowlers")
    bowlers_list_of_tuples = c.fetchall()
    
    # Create a list of bowlers
    bowlers = []
    for bowler in bowlers_list_of_tuples:
        bowlers.append(bowlers_list_of_tuples[0])

    # Close the cursor and the database connection
    c.close()
    conn.close()

    return render_template("bowler_comparisons.html")


@app.route('/bowler_leaderboard')
def bowler_leaderboard():

    # Connect to the SQL database
    database_path = os.path.join("/mnt/c/WINDOWS/system32/CS50-Final-Project/bowlers", "sql_database", "bowlers.db")
    conn = sqlite3.connect(database_path)

    # Create a cursor
    c = conn.cursor()

    # Query the top 10 bowlers by your statistic
    c.execute("SELECT name, overs, economy, average, prop_score FROM bowlers ORDER BY prop_score LIMIT 10")
    top_10 = c.fetchall()

    # Close the cursor and the database connection
    c.close()
    conn.close()

    # Render template
    return render_template("bowler_leaderboard.html", top_10=top_10)


if __name__ == '__main__':
    app.run(debug=True)