#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a dictionary of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def clean_array(temp_array):
    final_array = []
    remove_these = ["Pocock", "Forster", "Couzijn", "Thorell", "Peckham"]
    for strings in temp_array:
        temp_string = strings.replace("*", "").strip()
        for r in remove_these:
            if r in strings:
                temp_string = temp_string.split(r)[0].strip()
            if temp_string[-1:] == "(":
                temp_string = temp_string[:-1].strip()
        final_array.append(temp_string.strip())
    return final_array


def process_file(filename, fields):
    process_fields = fields.keys()

    data = []

    class_fields = ["class", "family", "genus", "kingdom", "order", "phylum"]

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()
        for line in reader:

              # Create new dictionary structure containing only the fields that are passed in.
            temp_dict = {}
            class_dict = {}
            for old_key in process_fields:
                new_key = fields[old_key]
                if new_key in ["label", "uri", "description", "name", "synonym"]:
                    temp_dict[new_key] = line[old_key].strip()
                else:
                    class_dict[new_key] = line[old_key].strip()
                    if class_dict[new_key] == "NULL":
                        class_dict[new_key] = None

            temp_dict["classification"] = class_dict

            for new_field in temp_dict.keys():

                  # Remove (extra names) from labels
                if new_field == "label":
                    temp_dict["label"] = temp_dict["label"].split("(")[0].strip()

                  # Check for non-alphanumeric chars, if found, replace "name" with "label"
                if new_field == "name":
                    if re.search('[A-Za-z0-9]*', temp_dict[new_field]).group() != temp_dict[new_field]:
                        temp_dict[new_field] = temp_dict["label"].strip()

                  # Change all NULL entries to None, except in "name" where NULL is changed to "label" entry.
                if temp_dict[new_field] == "NULL":
                    if new_field == "name":
                        temp_dict[new_field] = temp_dict["label"].strip()
                    else:
                        temp_dict[new_field] = None
                  # Split synonyms into list of synonyms. Pass to clean_array() for further cleaning.
                if new_field == "synonym" and temp_dict["synonym"] is not None:
                    temp_array = parse_array(temp_dict["synonym"])
                    temp_dict["synonym"] = clean_array(temp_array)

            data.append(temp_dict)

    return data


def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None,
        "name": "Argiope",
        "classification": {
            "kingdom": "Animal",
            "family": "Orb-weaver spider",
            "order": "Spider",
            "phylum": "Arthropod",
            "genus": None,
            "class": "Arachnid"
        },
        "uri": "http://dbpedia.org/resource/Argiope_(spider)",
        "label": "Argiope",
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }


if __name__ == "__main__":
    test()