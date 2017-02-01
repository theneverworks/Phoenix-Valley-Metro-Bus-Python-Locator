from google.transit import gtfs_realtime_pb2
import requests
import time
import os
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def findbus():
    message = request.args.get('s', None)
    busroute = message.upper()

    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('https://transitdata.phoenix.gov/api/vehiclepositions')
    feed.ParseFromString(response.content)
    finalresponse = "["
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            if (entity.vehicle.trip.route_id == busroute):
                finalresponse += "{'route':'" + str(entity.vehicle.trip.route_id) + "',"
                finalresponse += "'trip':'" + entity.vehicle.trip.trip_id + "',"
                if entity.vehicle.current_status == 0:
                    finalresponse += "'current_status':'Approaching stop',"
                if entity.vehicle.current_status == 1:
                    finalresponse += "'current_status':'At stop',"
                if entity.vehicle.current_status == 2:
                    finalresponse += "'current_status':'Departed for next stop',"
                try:
                    finalresponse += "'current_stop':'" + entity.vehicle.stop_id + "',"
                except:
                    finalresponse += "'current_stop':'No stop information available',"
                finalresponse += "'vehicle':'" + str(entity.vehicle.vehicle.id) + "',"
                finalresponse += "'licenseplate':'" + str(entity.vehicle.vehicle.license_plate) + "',"
                finalresponse += "'lat':'" + str(entity.vehicle.position.latitude) + "',"
                finalresponse += "'lon':'" + str(entity.vehicle.position.longitude) + "',"
                finalresponse += "'busmap':'https://www.google.com/maps/place/" + str(entity.vehicle.position.latitude) + "," + str(entity.vehicle.position.longitude) + "',"
                finalresponse += "'speed':'" + str(entity.vehicle.position.speed*2.23694) + " MPH',"
                finalresponse += "'bearing':'" + str(entity.vehicle.position.bearing) + " degrees from North',"
                if entity.vehicle.congestion_level == 0:
                    finalresponse += "'congestion Level':'Unknown',"
                if entity.vehicle.congestion_level == 1:
                    finalresponse += "'congestion Level':'Smooth',"
                if entity.vehicle.congestion_level == 2:
                    finalresponse += "'congestion Level':'Stop and Go',"
                if entity.vehicle.congestion_level == 3:
                    finalresponse += "'congestion Level':'Congested',"
                if entity.vehicle.congestion_level == 4:
                    finalresponse += "'congestion Level':'Severe Congestion',"
                finalresponse += "'updated':'" + time.strftime('%m-%d-%Y %H:%M:%S', time.localtime((entity.vehicle.timestamp))) + "'},"
        if entity.HasField('alert'):
            finalresponse += "{'alert':'" + str(entity.vehicle.trip.route_id) + "'},"
    finalresponse += "]"
    if finalresponse == "[]":
        finalresponse = "{'nobus':'" + busroute + "'}"
    response.headers['Content-Type'] = 'application/json' 
    return finalresponse

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)