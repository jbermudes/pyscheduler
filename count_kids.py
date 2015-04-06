#!/usr/bin/env python

from __future__ import print_function, division

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="CSV file to use as input")
    parser.add_argument("prefix", help="prefix for output files")
    parser.add_argument("-t", "--tab", help="use Tab delimiter instead", action='store_true')
    args = parser.parse_args()

    use_tab = args.tab
    filename = args.file
    out_prefix = args.prefix
    studio_roster_filename = str(out_prefix) + "_studio_roster.csv"
    dancer_roster_filename = str(out_prefix) + "_dancer_roster.csv"
    summary_filename = str(out_prefix) + "_summary.txt"
    #print "Working with file %s" % (filename)

    print("Working Directory is %s" % os.getcwd())

    if use_tab:
        delimiter = '\t'
    else:
        delimiter = ','
      
    entries = load_entries(filename)

    # all_dances["Bob"] = [num_nongroups, num_groups, total, routines]
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
              all_dancers[dancer] = [0,0,0,[]]
            all_dancers[dancer][2] += 1
            all_dancers[dancer][3].append(entry)
            if is_group:
                all_dancers[dancer][1] += 1
            else:
                all_dancers[dancer][0] += 1

        if is_group:
            total_group_dancers += len(entry.dancers)


    # Write Dancer Roster by Studio
    print("Writing Dancer Roster by Studio")

    with open(studio_roster_filename, "w") as f_studio:
        print("Studio,Dancer,Non-Groups,Groups,Total", file=f_studio)
        for studio_name in studios:
            for dancer in studios[studio_name]:
              dancer_data = all_dancers[dancer]
              print("%s,%s,%d,%d,%d" % (studio_name, dancer, dancer_data[0], 
                    dancer_data[1], dancer_data[2]), file=f_studio)
            studio_counts.append("%s, %d" % (studio_name, len(studios[studio_name])))

        print("", file=f_studio)

    # Write Dancer Roster with each dancer's routines
    print("Writing Dancer Roster with Routines")

    with open(dancer_roster_filename, "w") as f_dancer:
        print("ID\tAct\tStudio\tRoutine Name\tDancer", file=f_dancer)
        for studio_name in studios:
            for dancer in studios[studio_name]:
              dancer_data = all_dancers[dancer]
              for entry in dancer_data[3]:
                  print("%s\t%s\t%s\t%s\t%s" % (entry.entry_id, entry.act, 
                      studio_name, entry.routine_name, dancer), file=f_dancer)
        print("", file=f_dancer)        

    #Write Summary File with Studio totals and award count estimates
    print("Writing Summary File")

    with open(summary_filename, "w") as f_summary:
        print("Studio Totals:", file=f_summary)
        for line in studio_counts:
            print(line, file=f_summary)

        print("\nEvent Totals:", file=f_summary)
        print("Total Unique Dancers at Event: %d" % len(all_dancers), file=f_summary)
        print("Total Group pins: %d" % total_group_dancers, file=f_summary)
        print("", file=f_summary)        

if __name__ == "__main__":
    main()

