from google.transit import gtfs_realtime_pb2
import requests
import time
import sys

busroute = ' '.join(sys.argv[1:])
busroute = busroute.upper()

feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://transitdata.phoenix.gov/api/vehiclepositions')
feed.ParseFromString(response.content)
finalresponse = "Searching for route " + busroute
for entity in feed.entity:
    if entity.HasField('vehicle'):
        if (entity.vehicle.trip.route_id == busroute):
            finalresponse += "\nRoute " + str(entity.vehicle.trip.route_id) + "\n"
            finalresponse += "Trip " + entity.vehicle.trip.trip_id + "\n"
            if entity.vehicle.current_status == 0:
                finalresponse += "Approaching stop\n"
            if entity.vehicle.current_status == 1:
                finalresponse += "At stop\n"
            if entity.vehicle.current_status == 2:
                finalresponse += "Departed for next stop\n"
            try:
                finalresponse += "Current stop " + entity.vehicle.stop_id + "\n"
            except:
                finalresponse += "No stop information available\n"
            finalresponse += "Vehicle " + str(entity.vehicle.vehicle.id) + "\n"
            finalresponse += "License Plate " + str(entity.vehicle.vehicle.license_plate) + "\n"
            finalresponse += "Location " + str(entity.vehicle.position.latitude) + "," + str(entity.vehicle.position.longitude) + "\n"
            finalresponse += "Bus Location Map: " + "https://www.google.com/maps/place/" + str(entity.vehicle.position.latitude) + "," + str(entity.vehicle.position.longitude) + "\n"
            finalresponse += "Speed " + str(entity.vehicle.position.speed*2.23694) + " MPH\n"
            finalresponse += "Bearing " + str(entity.vehicle.position.bearing) + " degrees from North\n"
            if entity.vehicle.congestion_level == 0:
                finalresponse += "Congestion Level: Unknown\n"
            if entity.vehicle.congestion_level == 1:
                finalresponse += "Congestion Level: Smooth\n"
            if entity.vehicle.congestion_level == 2:
                finalresponse += "Congestion Level: Stop and Go\n"
            if entity.vehicle.congestion_level == 3:
                finalresponse += "Congestion Level: Congested\n"
            if entity.vehicle.congestion_level == 4:
                finalresponse += "Congestion Level: Severe Congestion\n"
            finalresponse += "Updated " + time.strftime('%m-%d-%Y %H:%M:%S', time.localtime((entity.vehicle.timestamp))) + "\n"
            finalresponse += "-------------------------------------\n"
    if entity.HasField('alert'):
        finalresponse += "Alert on Route " + str(entity.vehicle.trip.route_id)
        finalresponse += "-------------------------------------\n"
if finalresponse == "Searching for route " + busroute:
    finalresponse = "No bus is currently servicing route " + busroute
print finalresponse