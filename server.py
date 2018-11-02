import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, Table, and_
from flask import Flask, jsonify
import datetime as dt
import json



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)




@app.route("/")
def home():

    return (
        f"We have data from 2010-1-1 to 2017-8-23 for all your travel planning needs<br/>"
	
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
	f"You need to input dates as follows: 2010-01-31<br/>"
        "/api/v1.0/start/{start}"

	f"             This returns MIN, AVG, MAX temps since start<br/>"
	"/api/v1.0/range/{start}-{end}"
	f"             This returns MIN, AVG, MAX temps in range Start-END"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    yeardata = session.query(Measurement.date, Measurement.prcp).all()
    key=[yeardata[i][0] for i in range(len(yeardata))]
    values=[yeardata[i][1] for i in range(len(yeardata))]
    results=dict(zip(key,values))
    return jsonify(results)



@app.route("/api/v1.0/stations")
def stations():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Station = Base.classes.station
    session = Session(engine)
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)

    yearF_last_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    totalobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= yearF_last_date).all()

    key=[totalobs[i][0] for i in range(len(totalobs))]
    values=[totalobs[i][1] for i in range(len(totalobs))]
    results=dict(zip(key,values))
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    
    canonicalized = start.replace(" ", " ")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).all()

    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def calc_range(start, end):
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    
    canonicalized = start.replace(" ", " ")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(and_(Measurement.date >=start, Measurement.date <=end)).all()

    return jsonify(results)


   
if __name__ == '__main__':
    app.run(debug=True)
