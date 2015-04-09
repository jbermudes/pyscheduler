#!/usr/bin/env python

from __future__ import division
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

def bresenham_distribute(lists):
    while len(lists) > 1:
        lists = sorted(lists, key = lambda li: len(li), reverse=True)

        # Once lists are sorted, grab largest and 2nd largest
        dest = lists[0]
        src = lists[1]

        offset = len(dest) / len(src)
        counter = 0

        # copy src into dest evenly
        for item in src:
            counter += offset
            i = int(round(counter))
            dest.insert(i, item)
            counter += 1

        # delete src since we've already copied it into dest
        del lists[1]

    return lists[0]
 
def distribute_studios(entries):
  entries.sort(key= lambda e: e.studio)
  
  studios = []
  for k,g in itertools.groupby(entries, lambda e: e.studio):
    studios.append(list(g))

  #entries = list(round_robin_shuffle(*studios))
  entries = bresenham_distribute(studios)
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

  return sorted_entries

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="CSV file to use as input")
  parser.add_argument("-d", "--distance", help="the minimum distance to space routines", type=int, default=3)
  parser.add_argument("-s", "--shuffle", help="shuffle studios before scheduling", action="store_true")
  parser.add_argument("-o", "--output", help="the file to use for the new schedule", action="store_true")
  parser.add_argument("-c", "--check", help="check the file for conflicts, but do not schedule", action="store_true")
  parser.add_argument("-r", "--randomize", help="Randomly shuffle acts before studio shuffle", action="store_true")
  args = parser.parse_args()

  min_distance = args.distance
  filename = args.file
  #out_filename = args.output
  do_export = args.output
  print "Input file:  %s" % (filename)

  file_dir = os.path.dirname(filename)
  base = os.path.basename(filename)
  base_components = os.path.splitext(base)

  out_filename = os.path.join(file_dir, base_components[0] + '.sorted.csv')
  if do_export:
    print "Output file: %s" % out_filename

  print
      
  unsorted_entries = load_entries(filename)

  if args.check:
    c = scheduler.count_conflicts(unsorted_entries, min_distance)
    print "%d conflicts found.\n" % c
    print "Check complete. Terminating..."
    sys.exit(0)

  if args.randomize:
    seed = random.randint(0, sys.maxint)
    rng = random.Random(seed)
    print "Randomizing input with seed %d ..." % seed
    rng.shuffle(unsorted_entries)
    #unsorted_entries = distribute_studios(unsorted_entries)
  
  print "%d entries found.\n" % len(unsorted_entries)

  c = scheduler.count_conflicts(unsorted_entries, min_distance)

  print "%d conflicts found.\n" % c

  if c > 0:
    print "Shuffling Studios..."
    unsorted_entries = distribute_studios(unsorted_entries)
    sorted_entries = schedule(unsorted_entries, min_distance)
  else:
    sorted_entries = unsorted_entries

  if args.randomize:
    print "RNG seed was %d" % seed

  if do_export:
    print "Writing results to file: %s" % out_filename
    export_entries(sorted_entries, out_filename)
  else:
    print "No export requested. Terminating..."



