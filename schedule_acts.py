#!/usr/bin/env python

import csv
import os
import sys
import scheduler
from entry import Entry
from pprint import pprint


def load_entries(filename):
  with open(filename, 'rb') as csvfile:
    tsvreader = csv.DictReader(csvfile, delimiter='\t')
    entries = []
    for row in tsvreader:
      dancers_str = row["dancer_roster"]
      dancers = dancers_str.split(',')
      dancers = [x.strip() for x in dancers]
      entry = Entry(row, dancers)
      entries.append(entry)
  return entries

def export_entries(entries, filename):
  with open(filename, "wb") as csvfile:
    csvfile.write(Entry.csv_header('\t'))
    for entry in entries:
      csvfile.write(entry.to_csv('\t'))

if __name__ == "__main__":
  min_distance = int(sys.argv[1])
  filename = sys.argv[2]
  out_filename = sys.argv[3]
  print "Working with file %s" % (filename)
      
  unsorted_entries = load_entries(filename)
  
  print "%d entries found.\n" % len(unsorted_entries)

  c = scheduler.count_conflicts(unsorted_entries, min_distance)

  print "%d conflicts found.\n" % c

  sorted_entries = scheduler.do_schedule(unsorted_entries, min_distance)
  
  c2 = scheduler.count_conflicts(sorted_entries, min_distance)

  print "%d conflicts remain.\n" % c2

  if c2 > 0:
    print "Trying reverse traversal"
    list2 = sorted_entries
    list2.reverse()
    
    sorted2 = scheduler.do_schedule(list2, min_distance)
    sorted2.reverse()

    c3 = scheduler.count_conflicts(sorted2, min_distance)

    print "After reverse scheduling, %d conflicts remain.\n" % c3

    if c3 < c2:
      sorted_entries = sorted2

  export_entries(sorted_entries, out_filename)

