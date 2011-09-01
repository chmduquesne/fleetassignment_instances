#!/usr/bin/env python
"""
This program turns an IFAM instance into a FAM instance.

USAGE:

    ifam_to_fam [options] <ifam instance>

OPTIONS:

    -h, --help:         Print this help text

    Use "-" to read the ifam input instance from stdin

HOW IT WORKS:

    A rough estimation of the spill cost for assigning the model m to the
    leg l is made using the following formula:

    spillcost_{m, l} = max(0, D_l - C_m) * avgfare_l * kappa

    D_l is the aggregated demand on l, C_m is the cumulated capacity of
    all the cabins on m, and avgfare_l is the average fare on l. Kappa is
    a dimensionless quantity experimentally determined by Timothy S.
    Kniker and is taken equals to 0.7.

    The assignment cost is computed by summing operating cost and spill
    cost.

    Even if provided, recapture rates are skipped.
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
        # 1) compute D_l
        itineraries_crossing_l = [
                i for i, v in instance["itineraries"].items()
                if l in [leg["leg"] for leg in v]
                ]
        D_l = sum([instance["demand"][i] for i in itineraries_crossing_l])
        # 2) compute avgfare_l
        try:
            avgfare_l = sum([instance["fare"][i]*instance["demand"][i]
                for i in itineraries_crossing_l]) / D_l
        except ZeroDivisionError:
            # No demand on the flight, true in some instances
            avgfare_l = 0
        for m in instance["fleet"].keys():
                # 3) compute C_m
                C_m = sum(instance["fleet"][m]["capacity"].values())
                # 4) update the cost
                spillcost_m_l = max(0, D_l - C_m) * avgfare_l * kappa
                result["assignmentcost"][l][m] += spillcost_m_l

    for m in result["fleet"].keys():
        del result["fleet"][m]["capacity"]

    return result

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError, err:
        print str(err)
        print __doc__
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print __doc__
            sys.exit()

    source = "".join(args)
    if not source:
        print __doc__
        sys.exit()
    if source == "-":
        stream = sys.stdin
    else:
        stream = open(source)
    with stream:
        instance = json.load(stream)
        modifiedInstance = modify(instance)
        print json.dumps(modifiedInstance, indent = 4)

if __name__ == "__main__":
    main()
