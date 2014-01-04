#!/usr/bin/env python

import argparse
import csv
import itertools
import os
import random
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

def round_robin_shuffle(*iterables):
  num_lists = len(iterables)
  dst = []
  while num_lists > 0:
    if num_lists > 1:
      # distribute via round robin
      for li in iterables:
        if len(li) > 0:
          dst.append(li.pop(0))
      iterables = filter(None, iterables)
      num_lists = len(iterables)
    else:
      # distribute last stack throughout list
      li = iterables[0]
      i = 1
      while len(li) > 0:
        dst.insert(i, li.pop(0))
        if len(li) > 0:
          i = (i+2) % len(dst)
        else:
          # li is empty, we're done
          num_lists = 0

  return dst

 
def distribute_studios(entries):
  entries.sort(key= lambda e: e.studio)
  
  studios = []
  for k,g in itertools.groupby(entries, lambda e: e.studio):
    studios.append(list(g))

  entries = list(round_robin_shuffle(*studios))
  return entries

def schedule(entries, min_distance):
  sorted_entries = scheduler.do_schedule(entries, min_distance)
  
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

  return entries

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="CSV file to use as input")
  parser.add_argument("-d", "--distance", help="the minimum distance to space routines", type=int, default=3)
  parser.add_argument("-o", "--output", help="the file to use for the new schedule", type= str)
  args = parser.parse_args()

  min_distance = args.distance
  filename = args.file
  out_filename = args.output
  print "Working with file %s" % (filename)
      
  unsorted_entries = load_entries(filename)
  random.shuffle(unsorted_entries)
  unsorted_entries = distribute_studios(unsorted_entries)
  
  print "%d entries found.\n" % len(unsorted_entries)

  c = scheduler.count_conflicts(unsorted_entries, min_distance)

  print "%d conflicts found.\n" % c

  sorted_entries = schedule(unsorted_entries, min_distance)

  #Entry.__eq__ = lambda a,b: a.studio == b.studio
  #print "Attempting studio spacing\n"
  #sorted_entries = schedule(sorted_entries, min_distance)
  if out_filename:
    export_entries(sorted_entries, out_filename)

