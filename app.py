import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################


@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"<h1>Available Routes:</h1><br/>"
        f"<h2>/api/v1.0/precipitation</h2><br/>"
        f"<h2>/api/v1.0/stations</h2><br/>"
        f"<h2>/api/v1.0/tobs</h2><br/>"
        f"<h2>/api/v1.0/start</h2>    where start is the starting date to beging to analyze, use ISO format YYYY-MM-DD <br/>"
        f"<h2>/api/v1.0/start/end</h2>   start and end are the starting and ending date for analysis, use ISO format YYYY-MM-DD"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Convert the query results to a dictionatary using de as the key and prcp as the value and Return the JSON representation of your dictionar"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_dates = []
    for date, pcpt in results:
        pcpt_dict = {}
        pcpt_dict["date"] = date
        pcpt_dict["pcpt"] = pcpt
        all_dates.append(pcpt_dict)
    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Station.station).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
   # all_passengers = []
    # for name, age, sex in results:
    #     passenger_dict = {}
    #     passenger_dict["name"] = name
    #     passenger_dict["age"] = age
    #     passenger_dict["sex"] = sex
    #     all_passengers.append(passenger_dict)
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Calculate dates
    # recent = []
    # year_ago = []
    recent = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()
    recent = recent[0]
    year_ago = dt.date.fromisoformat(recent) - dt.timedelta(days=365)
    # Query all stations
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(func.strftime("%Y-%m-%d", Measurement.date) <= recent).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= year_ago).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
   # all_passengers = []
    # for name, age, sex in results:
    #     passenger_dict = {}
    #     passenger_dict["name"] = name
    #     passenger_dict["age"] = age
    #     passenger_dict["sex"] = sex
    #     all_passengers.append(passenger_dict)
    return jsonify(results)


# @app.route("/api/v1.0/<start>/<end>")
# def by_date(start, end):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
#     """Return a JSON list of temperature observations (TOBS) for the previous year."""
#     # Query all stations
#     results = session.query(Measurement.tobs, Measurement.date).all()
#     session.close()
#     for date in results:
#         # Create a dictionary from the row data and append to a list of all_passengers
#        # all_passengers = []
#         # for name, age, sex in results:
#         #     passenger_dict = {}
#         #     passenger_dict["name"] = name
#         #     passenger_dict["age"] = age
#         #     passenger_dict["sex"] = sex
#         #     all_passengers.append(passenger_dict)
#         return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
