#!/usr/bin/env python
"""
This program perturbs the demands on an IFAM instance.
"""
import json
import getopt
import sys
import os
import math
import random

def truncate(number, mini=-sys.maxint-1, maxi=sys.maxint):
    """
    returns number, or min/max if number is out of min-max range
    """
    return min(maxi, max(mini, number))

def modify(instance, perturbation = 0.0):

    assert instance["instance"] == "IFAM", "Only works on IFAM instances."
    assert perturbation >= 0, "Perturbation has to be >= 0"

    demand = instance["demand"]
    for i in demand.keys():
        epsilon = random.normalvariate(0, perturbation * demand[i])
        demand[i] = demand[i] + epsilon
        demand[i] = truncate(demand[i], mini=0)

    return instance

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "demand="])
    except getopt.GetoptError, err:
        print str(err)
        print __doc__
        sys.exit(2)

    perturbation = 0

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print __doc__
        if opt in ("-d", "--demand"):
            perturbation = float(arg)

    source = "".join(args)
    assert source != "", "No source provided"
    if source == "-":
        stream = sys.stdin
    else:
        stream = open(source)
    with stream:
        instance = json.load(stream)
        modifiedInstance = modify(instance, perturbation)
        print json.dumps(modifiedInstance, indent = 4)

