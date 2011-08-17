#!/usr/bin/env python
"""
This script reads a *FAM instance and prints some stats about the size of
the instance.
"""
import os
import sys
import simplejson as json

if __name__ == "__main__":
    instance = sys.argv[1]
    f = open(instance)
    d = json.load(f)

    instance_type = d["instance"]
    print ("%s is a %s instance" % (instance, instance_type))
    print ("number of legs: %d" % len(d["network"]))
    print ("number of aircraft types: %d" % len(d["fleet"]))
    if instance_type != "FAM":
        print ("number of itineraries: %d" % len(d["itineraries"]))
