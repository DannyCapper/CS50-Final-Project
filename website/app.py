import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from pathlib import Path
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect

class BowlerSearchForm(FlaskForm):
    bowler_search = StringField('Bowler Search', validators=[DataRequired()])

# Configure application
app = Flask(__name__)
app.secret_key = 'secret_key'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/context')
def context():
    return render_template("context.html")


@app.route('/data_and_methodology')
def data_and_methodology():
    return render_template("data_and_methodology.html")


@app.route('/results')
def results():
    return render_template("results.html")


@app.route('/bowler_comparisons', methods=['GET', 'POST'])
def search_bowler():
    form = BowlerSearchForm()
    error_messages = []

    # Initialize the bowler_stats_list in the session if it doesn't exist
    if 'bowler_stats_list' not in session:
        session['bowler_stats_list'] = []

    # Get the list of all bowlers
    all_bowlers = fetch_all_bowlers_data()

    if form.validate_on_submit():
        # Check if there are already 5 bowlers in the list
        if len(session['bowler_stats_list']) >= 5:
            error_messages.append("You can't compare more than 5 bowlers at a time. Please reset to compare a new set of bowlers.")
        else:
            # Get the list of bowler_stats based on the search input
            search_input = form.bowler_search.data
            bowler_stats = get_bowler_stats(search_input)

            # Check if a bowler is found, otherwise display a message
            if bowler_stats:
                session['bowler_stats_list'].append(bowler_stats)
                session.modified = True
            else:
                error_messages.append(f"Bowler '{search_input}' not found. Please try again with a different name.")

    return render_template("bowler_comparisons.html", form=form, bowler_stats_list=session['bowler_stats_list'], all_bowlers=all_bowlers, error_messages=error_messages)
def get_bowler_stats(search_input):
    
    # Here, we need the list of dictionaries to come in
    bowlers = fetch_bowler_data()

    # Extract the searched for bowler and their stats
    for bowler_stats in bowlers:
        if bowler_stats["name"] == search_input:
            return bowler_stats
            

def fetch_all_bowlers_data():

   # Set directory path for database
    db_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/bowlers/sql_database/bowlers.db")

    # Connect to the database
    with sqlite3.connect(db_path) as conn:
    
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute the query
        all_bowlers = cursor.execute("SELECT name FROM bowlers").fetchall()

        # Convert tuples to a list of strings
        all_bowlers = [bowler[0] for bowler in all_bowlers]

         # Return bowler data
        return all_bowlers


def fetch_bowler_data():

    # Set directory path for database
    db_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/bowlers/sql_database/bowlers.db")

    # Connect to the database
    with sqlite3.connect(db_path) as conn:
    
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute the query
        rows = cursor.execute("SELECT name, economy, average, prop_score FROM bowlers").fetchall()

        # Convert each tuple into a dictionary
        bowler_stats = []
        for row in rows:
            bowler = {
                "name": row[0],
                "economy": row[1],
                "average": row[2],
                "prop_score": row[3]
            }
            bowler_stats.append(bowler)

    # Return bowler data
    return bowler_stats


@app.route('/reset_bowler_comparisons', methods=['GET'])
def reset_bowler_comparisons():
    session['bowler_stats_list'] = []
    return redirect(url_for("search_bowler"))


@app.route('/bowler_leaderboard')
def bowler_leaderboard():

    # Set the directory path for the database
    database_path = Path("/mnt/c/USERS/danny/CS50-Final-Project/bowlers/sql_database/bowlers.db")

    # Connect to the SQL database
    with sqlite3.connect(database_path) as conn:

        # Create a cursor
        c = conn.cursor()

    # Query the top 10 bowlers by your statistic
    c.execute("SELECT name, overs, economy, average, prop_score FROM bowlers WHERE overs > 100 ORDER BY prop_score LIMIT 10")
    top_10 = c.fetchall()

    # Close the cursor and the database connection
    c.close()
    conn.close()

    # Render template
    return render_template("bowler_leaderboard.html", top_10=top_10)


if __name__ == '__main__':
    app.run(debug=True)