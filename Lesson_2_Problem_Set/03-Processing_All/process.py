#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    """
    This function extracts data from the file given as the function argument in
    a list of dictionaries. This is example of the data structure you should
    return:

    data = [{"courier": "FL",
             "airport": "ATL",
             "year": 2012,
             "month": 12,
             "flights": {"domestic": 100,
                         "international": 100}
            },
            {"courier": "..."}
    ]


    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list
    # will be a reference to the same info dictionary.
    with open("{}/{}".format(datadir, f), "r") as html:

        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", class_="dataTDRight")
        values = []
        # iterate through our table, skipping the first row because that doesn't contain any data we want
        for rows in table.find_all("tr")[1:]:
            cells = rows.find_all("td")
            new_cells = []
            # we have all the data in 'cells', this will get rid of those pesky commas
            for col in cells:
                new_cells.append(col.text.replace(",",""))
            # if you thought the commas were bad, those TOTAL rows were something else...
            if new_cells[1] != "TOTAL":
                # we need convert everything from strings to integers
                values = map(int, new_cells)
                data.append({"courier": "FL",
                             "airport": "ATL",
                             "year": values[0],
                             "month": values[1],
                             "flights": {"domestic": values[2],
                                         "international": values[3]}
                            })

    return data


def test():
    print "Running a simple test..."
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
    assert len(data) == 3
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    print "... success!"

if __name__ == "__main__":
    test()