#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the datatypes that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint
import re
from collections import defaultdict

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]


def is_int(value):
    """Returns True if if the value can be cast to int"""
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    """Returns True if if the value can be cast to float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def value_type(value):
    """ Returns
    - NoneType if the value is a string "NULL" or an empty string ""
    - list, if the value starts with "{"
    - int, if the value can be cast to int
    - float, if the value can be cast to float, but CANNOT be cast to int.
      For example, '3.23e+07' should be considered a float because it can be cast
      as float but int('3.23e+07') will throw a ValueError
    - 'str', for all other values
    """
    if value == "NULL" or "":
        return type(None)
    elif re.match(r'^{', value):
        return type([])
    elif is_int(value):  # Must be called before is_float
        return type(1)
    elif is_float(value):
        return type(1.1)
    else:
        return type('a')


def audit_file(filename, fields):
    fieldtypes = defaultdict(set)

    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        reader.next()
        reader.next()
        reader.next()
        for row in reader:
            for key, value in row.iteritems():
                fieldtypes[key].add(value_type(value))

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])


if __name__ == "__main__":
    test()
