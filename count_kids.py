#!/usr/bin/env python

import argparse
import csv
import itertools
import os
import random
import sys
from entry import Entry
from pprint import pprint


def load_entries(filename, my_delimiter='\t'):
  with open(filename, 'rb') as csvfile:
    tsvreader = csv.DictReader(csvfile, delimiter=my_delimiter)
    entries = []
    for row in tsvreader:
      dancers_str = row["dancer_roster"]
      dancers = dancers_str.split(',')
      dancers = [x.strip() for x in dancers]
      entry = Entry(row, dancers)
      entries.append(entry)
  return entries


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="CSV file to use as input")
  parser.add_argument("-t", "--tab", help="use Tab delimiter instead", action='store_true')
  args = parser.parse_args()

  use_tab = args.tab
  filename = args.file
  #print "Working with file %s" % (filename)

  if use_tab:
    delimiter = '\t'
  else:
    delimiter = ','
      
  entries = load_entries(filename)
  all_dancers = {}
  studios = {}
  total_group_dancers = 0 
  studio_counts = []

  for entry in entries:
    is_group = entry.is_group()

    if not studios.has_key(entry.studio):
      studios[entry.studio] = set()
    studios[entry.studio].update(entry.dancers)

    for dancer in entry.dancers:
      #print "%s | %s $" % (dancer, entry.studio)
      if not all_dancers.has_key(dancer):
        all_dancers[dancer] = [0,0,0]
      all_dancers[dancer][2] += 1
      if is_group:
        all_dancers[dancer][1] += 1
      else:
        all_dancers[dancer][0] += 1

    if is_group:
      total_group_dancers += len(entry.dancers)

  print "Studio,Dancer,Non-Groups,Groups,Total"
  for studio_name in studios:
    for dancer in studios[studio_name]:
      dancer_data = all_dancers[dancer]
      print "%s,%s,%d,%d,%d" % (studio_name, dancer, dancer_data[0], 
              dancer_data[1], dancer_data[2])
    studio_counts.append("%s, %d" % (studio_name, len(studios[studio_name])))

  print

  print "\nStudio Totals:"
  for line in studio_counts:
    print line

  print "\nEvent Totals:"
  print "Total Unique Dancers at Event: %d" % len(all_dancers)
  print "Total Group pins: %d" % total_group_dancers


