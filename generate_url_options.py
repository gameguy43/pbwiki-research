#!/bin/python
import csv
import os

wikid = csv.DictReader(open('./nocheckin/CodedWikis-1798.csv', 'r'), delimiter=';', quotechar='"')
wikil = []

for row in wikid:
    wikil.append(row['wikiname']);

for row in wikil:
    print row
