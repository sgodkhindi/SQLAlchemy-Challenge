# Import dependecies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import json
from flask import Flask, render_template, jsonify

# create engine to hawaii.sqlite
database_path="Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base=automap_base()

# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Import Flask
from flask import Flask, jsonify

# Flask setup
app=Flask(__name__)

# Flask routes
@app.route("/")
def home():
    """List all available api routes"""
    return (
            f"Shailesh Godkhindi's API Home Page<br/>"
            f"Here are the available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/2014-03-01<br/>"
            f"/api/v1.0/2010-01-01/2017-08-23<br/>"
            )

@app.route("/api/v1.0/precipitation")
def prcp():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    max_prcp = session.query(Measurement.date,func.max(Measurement.prcp)).filter(Measurement.date>="2016-08-23").\
    group_by(Measurement.date).all()
  
    session.close()
   
    all_prcp = []
    
    for date, prcp in max_prcp:
        all_prcp.append({date:prcp})
    
    # Jsonify the list
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
       
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all stations
    stations=session.query(Station.name).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    allstations = list(np.ravel(stations))

    # Jsonify the list
    return jsonify(allstations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Redirected to the Temperature of Observation Page"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all temperatures
    temps =session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>="2016-08-23").\
        filter(Measurement.station == 'USC00519281').all()

    # Close the session
    session.close()
    
    # Create a dictionary from the row data and append to a list of all_tobs
    alltobs=[]
        
    for date, tobs in temps:
        alltobs.append({date:tobs})

    # Jsonify the list
    return jsonify(alltobs)

@app.route("/api/v1.0/<start>")
def temp_start(start):
       
    # Create our session (link) from Python to the DB
    session = Session(engine)
      
    # Query the min, max and average temperatures
    temperatures=session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start).all()
        
        # Query all the dates within the database
    dates=session.query(Measurement.date).all()
        
        # Close the session   
    session.close()
    
    # Convert list of tuples into normal list
    all_dates=list(np.ravel(dates))
    
    #  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start 
    
    for start_date in all_dates:
            if start_date==start:
                results_start = {
                    "Start Date": start,
                    "End Date": "2017-08-23",
                    "Temperature Minimum": temperatures[0][1],
                    "Temperature Average": round(temperatures[0][3],1),
                    "Temperature Maximum": temperatures[0][2]
                }
                return jsonify([results_start])

    return jsonify([f"error: Data for '{start}'was not found"])

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
            
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all temperatures
    # sel=[Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    temperatures=session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    
    # Query all the dates within the database
    dates=session.query(Measurement.date).all()
    
    # Close the session   
    session.close()
    
    # Convert list of tuples into normal list
    all_dates=list(np.ravel(dates))
     
    for start_date in all_dates:
        if start_date==start:
            for end_date in all_dates:
                if end_date==end:
                    if end>start:
                        results_start_end = {
                            "Start Date": start,
                            "End Date": end,
                            "Temperature Minimum": temperatures[0][1],
                            "Temperature Average": round(temperatures[0][3],1),
                            "Temperature Maximum": temperatures[0][2]
                        }
                        return jsonify([results_start_end])
            return jsonify([f"error: Data for '{start} and '{end}'was not found"])          
    return jsonify([f"error: Data for '{start} and '{end}'was not found"])       

if __name__ == '__main__':
   app.run(debug=True, port=5002)