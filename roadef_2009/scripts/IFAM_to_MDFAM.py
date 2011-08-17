#!/usr/bin/env python
"""
This program turns an IFAM instance into a MDFAM instance.
"""
import json
import getopt
import sys
import os
import math

def modify(instance):
    result = {}

    result["instance"] = "MDFAM"
    result["network"] = instance["network"]
    result["cabins"] = instance["cabins"]
    result["fleet"] = instance["fleet"]
    result["operatingcost"] = instance["operatingcost"]
    result["itineraries"] = instance["itineraries"]
    result["fare"] = instance["fare"]

    result["groups"] = {}
    result["demand"] = {}
    for l in instance["network"].keys():
        # 1) compute G_l
        itineraries_crossing_l = [
                i for i, v in instance["itineraries"].items()
                if l in [leg["leg"] for leg in v]
                ]
        result["groups"][l] = itineraries_crossing_l
        result["demand"][l] = sum([instance["demand"][i] for i in itineraries_crossing_l])

    return result

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

    source = "".join(args)
    assert source != "", "No source provided"
    if source == "-":
        stream = sys.stdin
    else:
        stream = open(source)
    with stream:
        instance = json.load(stream)
        modifiedInstance = modify(instance)
        print json.dumps(modifiedInstance, indent = 4)

