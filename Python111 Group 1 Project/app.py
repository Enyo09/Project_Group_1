# from flask import Flask, render_template
# import pandas as pd

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/about")
# def about():
#     return render_template("aboutus.html")

# @app.route("/data")
# def data():
#     # Read the CSV file into a DataFrame
#     df = pd.read_csv("onlinefoods.csv")

#     # Convert DataFrame to list of dictionaries
#     data = df.to_dict(orient="records")

#     return render_template("data_details.html", data=data)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template
import pandas as pd
import sqlite3
import pathlib

app = Flask(__name__)

base_path = pathlib.Path(__file__).parent.resolve()
db_path = base_path / "onlinefoods.db"
csv_path = base_path / "onlinefoods.csv"

# Create the 'onlinefoods' table if it doesn't exist
def create_table():
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)

    # Create a table and insert the data from the DataFrame
    df.to_sql("onlinefoods", connection, if_exists="replace", index=False)

    # Close the database connection
    connection.close()

# Call the function to create the 'onlinefoods' table
create_table()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("aboutus.html")

@app.route("/data")
def data():
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Convert DataFrame to list of dictionaries
    data = df.to_dict(orient="records")

    return render_template("data_details.html", data=data)

@app.route("/query")
def query_database():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM onlinefoods")
    results = cursor.fetchall()
    connection.close()

    for row in results:
        print(row)

    query_message = "The 'SELECT * FROM onlinefoods' query has been executed successfully!"
    return render_template("query_results.html", message=query_message)

if __name__ == "__main__":
    app.run(debug=True)