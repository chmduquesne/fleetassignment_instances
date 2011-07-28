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


def to_datetime(start_datetime, text_delta):
    try:
        hh_mm, d = text_delta.split("+")
    except ValueError:
        hh_mm = text_delta
        d = "0"
    hh, mm = hh_mm.split(":")
    delta = datetime.timedelta(days=int(d), hours=int(hh), minutes=int(mm))
    return start_datetime + delta

def get_network(path):
    network = {}
    with open(os.path.join(path, "config.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        header = csvreader.next()
        start_date = dateutil.parser.parse(header[0])
    with open(os.path.join(path, "flights.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            try:
                id, boardpoint, offpoint, dep_time, arr_time, prec_flight = row
                network[id] = {
                        "boardpoint": boardpoint,
                        "offpoint": offpoint,
                        "departuretime": to_datetime(start_date,
                            dep_time).isoformat(),
                        "arrivaltime": to_datetime(start_date,
                            arr_time).isoformat()
                        }
            except ValueError:
                pass
    return network

def get_fleet(path):
    fleet = {}
    with open(os.path.join(path, "aircraft.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            try:
                id, model, family, config, dist, cost_h = row[:6]
                try:
                    fleet[model + config]["numberofaircraft"] += 1
                except KeyError:
                    fir, bus, eco = config.split("/")
                    if int(fir)>=0 and int(bus) >=0 and int(eco)>=0:
                        fleet[model + config] = {
                                "numberofaircraft": 1,
                                "capacity": {
                                    "E": int(eco),
                                    "B": int(bus),
                                    "F": int(fir)
                                    },
                                "hourly_opcost": float(cost_h)}
            except ValueError:
                pass
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

def get_itineraries_fares_groups_demands(path):
    itineraries = {}
    fares = {}
    demands = {}
    with open(os.path.join(path, "itineraries.csv")) as f:
        csvreader = csv.reader(f, delimiter=' ')
        for row in csvreader:
            if len(row) > 1:
                nblegs = (len(row) - 5)/3
                id = row[0]
                itinerary = []
                for i in range(nblegs):
                    itinerary.append({"cabin": row[3*i + 6], "leg": row[3*i + 4]})
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

    instance["instance"] = "MDFAM"
    instance["network"] = get_network(path)
    instance["cabins"]= ["E", "B", "F"]
    instance["fleet"] = get_fleet(path)
    instance["operatingcost"] = get_operatingcosts(instance)
    instance["itineraries"], instance["fare"], instance["demand"] = \
            get_itineraries_fares_groups_demands(path)
    instance["correlations"] = {}

    clean_hourlyopcosts(instance)

    print json.dumps(instance, indent=4)
