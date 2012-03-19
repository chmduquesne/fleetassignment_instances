#!/usr/bin/env python2
"""
Usage:
    ./to_IFAM.py <path/to/instance_dir/>

Options:
    -h, --help: prints this help

This program takes a ROADEF 2009 instance as an argument and turns it into
a Barnhart's IFAM instance.
"""

from __future__ import with_statement
import sys
import getopt
import os
import os.path
import csv
import datetime
import dateutil.parser
try:
    import simplejson as json
except ImportError:
    import json


def isoformat(date, hour):
    refdate = dateutil.parser.parse(date)
    try:
        hh_mm, d = hour.split("+")
    except ValueError:
        hh_mm = hour
        d = "0"
    hh, mm = hh_mm.split(":")
    delta = datetime.timedelta(days=int(d), hours=int(hh), minutes=int(mm))
    return (refdate + delta).isoformat()

def get_network_fleetassignment(path):
    # 1) get generic flight legs
    flights = {}
    with open(os.path.join(path, "flights.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            if len(row) > 1:
                id, boardpoint, offpoint, dep_time, arr_time, prec_flight = row[:6]
                flights[id] = {
                        "boardpoint": boardpoint,
                        "offpoint": offpoint,
                        "departuretime": dep_time,
                        "arrivaltime": arr_time
                        }
    network = {}
    fleetassignment = {}
    # 2) differentiate the real legs per day
    with open(os.path.join(path, "rotations.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            if len(row) > 1:
                id, date, aircraft = row[:3]
                if not aircraft.startswith("TranspCom"):
                    leg = dict(flights[id])
                    leg["departuretime"] = isoformat(date,
                            leg["departuretime"])
                    leg["arrivaltime"] = isoformat(date,
                            leg["arrivaltime"])
                    network["_".join([id, date])] = leg
                    fleetassignment["_".join([id, date])] = aircraft
    return (network, fleetassignment)

def get_fleet(path):
    fleet = {}
    with open(os.path.join(path, "aircraft.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            if len(row) > 1:
                id, model, family, config, dist, cost_h = row[:6]
                try:
                    fleet[model + config]["numberofaircraft"] += 1
                except KeyError:
                    fir, bus, eco = config.split("/")
                    if not id.startswith("TranspCom"):
                        fleet[model + config] = {
                                "numberofaircraft": 1,
                                "capacity": {
                                    "E": int(eco),
                                    "B": int(bus),
                                    "F": int(fir)
                                    },
                                "hourly_opcost": float(cost_h)}
    return fleet

def get_operatingcosts(instance):
    operatingcost = {}
    for flight_id, flight_data in instance["network"].items():
        dep_time = dateutil.parser.parse(flight_data["departuretime"])
        arr_time = dateutil.parser.parse(flight_data["arrivaltime"])
        flight_duration = arr_time - dep_time
        for model, model_data in instance["fleet"].items():
            if operatingcost.get(flight_id, None) is None:
                operatingcost[flight_id] = {}
            operatingcost[flight_id][model] = (
                    float(flight_duration.seconds) *
                    model_data["hourly_opcost"]/3600
                    )
    return operatingcost

def get_itinerary_fares_demands(path):
    itineraries = {}
    fares = {}
    demands = {}
    with open(os.path.join(path, "itineraries.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            if len(row) > 1:
                # the leg-cabins are after the 4 first fields
                nblegs = (len(row) - 4)/3
                id = row[0]
                itinerary = []
                for i in range(nblegs):
                    itinerary.append({
                        "leg": "_".join([row[4 + 3*i], row[4 + (3*i + 1)]]),
                        "cabin": row[4 + (3*i + 2)],
                        })
                itineraries[id] = itinerary
                fares[id] = float(row[2])
                demands[id] = int(row[3])
    return (itineraries, fares, demands)

def clean_hourlyopcosts(instance):
    for model_data in instance["fleet"].values():
        del model_data["hourly_opcost"]

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError, err:
        print str(err)
        print __doc__
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print __doc__
            sys.exit()
        else:
            assert False, "Unhandled option"

    path = "".join(args)
    if path == "" or not os.path.exists(path):
        print "Invalid path provided."
        print __doc__
        sys.exit(2)

    instance = {}

    instance["instance"] = "IFAM"
    instance["network"], instance["fleetassignment"] = \
            get_network_fleetassignment(path)
    instance["cabins"]= ["E", "B", "F"]
    instance["fleet"] = get_fleet(path)
    instance["operatingcost"] = get_operatingcosts(instance)
    instance["itineraries"], instance["fare"], instance["demand"] = \
            get_itinerary_fares_demands(path)

    clean_hourlyopcosts(instance)

    print json.dumps(instance, indent=4)
