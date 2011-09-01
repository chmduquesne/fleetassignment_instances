#!/usr/bin/env python
"""
This program turns an IFAM instance into a MDFAM instance.

USAGE:

    ifam_to_mdfam [options] <ifam instance>

OPTIONS:

    -h, --help:                     Print this help text
    -u, --uncertainty= <float>      uncertainty of the demand (min, max)
                                    in % (5 = 5%)
    Use "-" to read the ifam input instance from stdin

HOW IT WORKS:

    Groups are built by legs (every itineraries that go through the same
    leg are in the same group). The demands (min and max) of each group
    are the sum of the demands of each itinerary.

    Even if provided, recapture rates are skipped.
"""
import json
import getopt
import sys
import os
import math

def truncate(number, mini=-sys.maxint-1, maxi=sys.maxint):
    """
    returns number, or min/max if number is out of min-max range
    """
    return min(maxi, max(mini, number))

def modify(instance, uncertainty=0.0):
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
        d = math.fsum([instance["demand"][i] for i in itineraries_crossing_l])
        result["demand"][l] = {
                "min": truncate(d - uncertainty * d, mini=0),
                "max": truncate(d + uncertainty * d, mini=0)
                }

    return result

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hu:", ["help",
            "uncertainty="])
    except getopt.GetoptError, err:
        print str(err)
        print __doc__
        sys.exit(2)

    uncertainty=0.0

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print __doc__
            sys.exit()
        if opt in ("-u", "--uncertainty"):
            uncertainty=float(arg)/100

    source = "".join(args)
    if not source:
        print __doc__
        sys.exit(-2)
    if source == "-":
        stream = sys.stdin
    else:
        stream = open(source)
    with stream:
        instance = json.load(stream)
        modifiedInstance = modify(instance, uncertainty)
        print json.dumps(modifiedInstance, indent = 4)

if __name__ == "__main__":
    main()
