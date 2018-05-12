#!/bin/python3
import json
from math import pi, asin, sqrt, sin, cos
from time import time

import requests
import argparse


def get_distance(lat2,lon2):
    dlat = abs((latitude - lat2)/180*pi)
    dlon = abs((longitude - lon2)/180*pi)
    dsigma = 2*asin(sqrt(sin(dlat/2)**2 +
                         cos(latitude/180*pi)*cos(lat2/180*pi)*sin(dlon/2)**2))
    return dsigma * 40001/2/pi


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Find details of the plane nearest to you.')
    parser.add_argument('latitude', type=float)
    parser.add_argument('longitude', type=float)

    args = parser.parse_args()
    latitude = args.latitude
    longitude = args.longitude

    # get data from https://opensky-network.org/api/states/all
    r = requests.get("https://opensky-network.org/api/states/all")
    data = json.loads(r.text)
    states = data['states']

    distances = list()
    for plane in states:
        if not isinstance(plane[6], float) or not isinstance(plane[5], float):
            distances.append(float('Inf'))
            continue
        distances.append(get_distance(plane[6], plane[5]))

    closest_indx = distances.index((min(distances)))
    closest = states[closest_indx]

    request_data = {'icao24': closest[0], 'begin': int(time()) - 3600 * 12, 'end': int(time()) + 3600 * 12}
    flight_data = requests.get("https://opensky-network.org/api/flights/aircraft", params=request_data).text

    flight_data = json.loads(flight_data)[0]

    print("Distance: {}".format(distances[closest_indx]))
    print("Callsign: {}".format(closest[1]))
    print("Latitude {} Longitude: {}".format(closest[6], closest[5]))
    print("Geometric Altitude: {}".format(closest[7]))
    print("Country of Origin: {}".format(closest[2]))
    print(("ICAO24 ID: {}".format(closest[0])))
    print("Departure Airport: {}".format(flight_data["estDepartureAirport"]))
    print("Arrival Airport: {}".format(flight_data["estArrivalAirport"]))
    print("FlightAware Link: https://flightaware.com/live/flight/{}".format(closest[1]))
