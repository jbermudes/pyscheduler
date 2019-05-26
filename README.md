# PyScheduler

A script to rearrange the rows of a CSV file of dance routine entries into
one ordered so as to minimize the number of conflicting routines.
Conflicting routines are those where a given performer would have to perform 
againt too close to their prior performance in the schedule.

This transformation is accomplished using an adaptation of
[Bresenham's Line
Algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm).

Licensed under the GPLv2.

## Usage:
`schedule_acts.py FILE [OPTIONS]`

### Options:
`-d`, `--distance`: the minimum distance to space routines

`-s`, `--shuffle`: shuffle studios before scheduling

`-o`, `--output`: the file to output the transformed schedule to

`-c`, `--check`: check the file for conflicts, but do not schedule

`-r`, `--randomize`: randomly shuffle acts before the studio shuffle

`-g`, `--seed`: Use a specific integer seed for the RNG
