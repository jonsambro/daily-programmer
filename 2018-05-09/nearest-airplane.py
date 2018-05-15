#!/usr/bin/python3
import json
from math import pi, asin, sqrt, sin, cos
from time import time

import requests
import argparse


def get_geodesic_distance(lat2, lon2):
    global latitude
    global longitude
    delta_latitude = abs((latitude - lat2)/180*pi)
    delta_longitude = abs((longitude - lon2)/180*pi)
    delta_sigma = 2*asin(sqrt(sin(delta_latitude/2)**2 +
                         cos(latitude/180*pi)*cos(lat2/180*pi)*sin(delta_longitude/2)**2))
    return delta_sigma * 40001/2/pi


def retrieve_state_of_all_flights():
    r = requests.get("https://opensky-network.org/api/states/all")
    data = json.loads(r.text)
    return data['states']


def calculate_distance_from_flights(states):
    distances = list()
    for plane in states:
        if not isinstance(plane[6], float) or not isinstance(plane[5], float):
            distances.append(float('Inf'))
            continue
        distances.append(get_geodesic_distance(plane[6], plane[5]))
    return distances


def retrieve_detailed_flight_data(icao24):
    request_data = {'icao24': icao24, 'begin': int(time()) - 3600 * 12, 'end': int(time()) + 3600 * 12}
    flight_data = requests.get("https://opensky-network.org/api/flights/aircraft", params=request_data).text
    flight_data = json.loads(flight_data)[0]
    return flight_data


def print_results(distance, closest_plane, flight_data):
    print("Distance: {:.3}km".format(distance))
    print("Callsign: {}".format(closest_plane[1]))
    print("Latitude {} Longitude: {}".format(closest_plane[6], closest_plane[5]))
    print("Geometric Altitude: {}".format(closest_plane[7]))
    print("Country of Origin: {}".format(closest_plane[2]))
    print(("ICAO24 ID: {}".format(closest_plane[0])))
    print("Departure Airport: {}".format(flight_data["estDepartureAirport"]))
    print("Arrival Airport: {}".format(flight_data["estArrivalAirport"]))
    print("FlightAware Link: https://flightaware.com/live/flight/{}".format(closest_plane[1]))


def parse_arguments():
    parser = argparse.ArgumentParser('Find details of the plane nearest to you.')
    parser.add_argument('latitude', type=float, nargs='?', default=44.555751)
    parser.add_argument('longitude', type=float, nargs='?', default=-80.932080)

    args = parser.parse_args()
    latitude = args.latitude
    longitude = args.longitude
    return latitude, longitude


def main():
    global latitude, longitude
    latitude, longitude = parse_arguments()
    states = retrieve_state_of_all_flights()
    distances = calculate_distance_from_flights(states)
    index_of_closest_plane = distances.index((min(distances)))
    closest_plane = states[index_of_closest_plane]
    flight_data = retrieve_detailed_flight_data(closest_plane[0])

    print_results(distances[index_of_closest_plane], closest_plane, flight_data)


if __name__ == "__main__":
    main()
