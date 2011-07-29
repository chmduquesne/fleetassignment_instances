#!/usr/bin/env python
"""
This program turns an IFAM instance into a FAM instance.

A rough estimation of the spill cost for assigning the model m to the leg
l is made using the following formula:

spillcost_{m, l} = max(0, D_l - C_m) * avgfare_l * kappa

D_l is the aggregated demand on l, C_m is the cumulated capacity of all
the cabins on m, and avgfare_l is the average fare on l. Kappa is a
dimensionless quantity experimentally determined by Timothy S. Kniker and
is taken equals to 0.7.

The assignment cost is computed by summing operating cost and spill cost.
"""
import json
import getopt
import sys
import os
import math

kappa = 0.7

def modify(instance):
    result = {}

    result["instance"] = "FAM"
    result["network"] = instance["network"]
    result["fleet"] = instance["fleet"]

    result["assignmentcost"] = instance["operatingcost"]
    for l in instance["network"].keys():
        for m in instance["fleet"].keys():
            # 1) compute D_l
            itineraries_crossing_l = [
                    i for i, v in instance["itineraries"].items()
                    if l in [leg["leg"] for leg in v]
                    ]
            D_l = sum([instance["demand"][i] for i in itineraries_crossing_l])
            # 2) compute C_m
            C_m = sum(instance["fleet"][m]["capacity"].values())
            # 3) compute avgfare_l
            avgfare_l = sum([instance["fare"][i]*instance["demand"][i]
                for i in itineraries_crossing_l]) / D_l
            spillcost_m_l = max(0, D_l - C_m) * avgfare_l * kappa
            result["assignmentcost"][l][m] += spillcost_m_l

    for m in result["fleet"].keys():
        del result["fleet"][m]["capacity"]

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
