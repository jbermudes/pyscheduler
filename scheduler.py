#!/usr/bin/env python

import random
import sys, os



#random.seed(sys.argv[1])


def count_conflicts(L, min_distance):
  num_conflicts = 0
  for k in xrange(len(L) - 1):
    conflict = check_conflict(L, k, min_distance)
    if conflict:
      print "Conflict found @ %d" % (k+2)
      num_conflicts += 1

  return num_conflicts


def check_conflict(L, start, min_distance):
  conflict = False
    
  if start < len(L) - min_distance - 1:
    upto = min_distance
  else:
    upto = len(L) - start - 1

  for j in xrange(1, upto + 1):
    if L[start] == L[start+j]:
      return True
  return False


def do_schedule(unscheduled_list, min_distance):
  if len(unscheduled_list) < min_distance:
    return unscheduled_list

  src = list(unscheduled_list)
  dst = []
  dst.append(src.pop(0))

  while len(src) > 0:
    dst_end = dst[-min_distance:]
    #print "\nsrc: ", src
    #print "dst: ", dst
    
    if src[0] not in dst_end:
      dst.append(src.pop(0))
    else:
      #print "Conflict found, trying strategy 1"
      # Strategy 1: search src for a suitable candidate
      candidate_found = False
      for k in xrange(len(src)):
        if src[k] not in dst_end:
          dst.append(src.pop(k))
          #print "Candidate found via strategy 1"
          candidate_found = True
          break

      if not candidate_found:
        # Strategy 2: Search dst backwards for a spot
        #print "Trying strategy 2"
        for k in xrange(1,len(dst)):
          dst_local_end = dst[-(k+min_distance):-k]
          #print "dst_local_end: ", dst_local_end
          if src[0] not in dst_local_end:
            dst.insert(-(k+min_distance), src.pop(0))
            candidate_found = True
            #print "Candidate found via strategy 2"
            break
        #sys.exit()

      if not candidate_found:
        # Could not find a good place for it, so stick it at the end
        #print "Giving up"
        dst.append(src.pop(0))

  return dst

if __name__ == "__main__":

  MIN_DISTANCE = 2
  schedule = []

  #schedule = [1,2,2,3,3,3,4,4,4,4,5,6,7,8,9,10]
  schedule = [1,2,3,1,4,5]

  #for k in xrange(1, 500):
  #  if random.random() < 0.2 and len(schedule) > 0:
  #    schedule.append(schedule[-1])
  #  else:
  #    schedule.append(k)
  #print list

  c = count_conflicts(schedule, MIN_DISTANCE)
  print "Before: %d conflicts\n" % c

  print "Scheduling...."
  sorted = do_schedule(schedule, MIN_DISTANCE)

  print

  c2 = count_conflicts(sorted, MIN_DISTANCE)
  print "After: %d conflicts\n" % c2


  if c2 > 0:
    print "Trying reverse traversal"
    list2 = sorted
    list2.reverse()

    sorted2 = do_schedule(list2, MIN_DISTANCE)
    sorted2.reverse()

    c3 = count_conflicts(sorted2, MIN_DISTANCE)

    print "\nAfter reverse schedule: %d conflicts" % c3

