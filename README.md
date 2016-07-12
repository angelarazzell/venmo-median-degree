
Calculate the median degree of a vertex in a Venmo transaction graph
====================================================================

Given a file input of Venmo transactions, this solution parses the transactions to:

- Build a graph of users and their relationship with one another.

- Calculate the median degree of a vertex in a graph and update this each time a new Venmo payment appears (i.e. each new line in the file). Calculates the median degree across a 60-second sliding window.

The vertices on the graph represent Venmo users and whenever one user pays another user, an edge is formed between the two users.

## How to run

1. Populate .venmo_input/venmo-trans.txt with JSON formatted transactions (currently populated in this repo)

2. Run ./run.sh in the topmost directory. This will run ./src/median_degree.py and write the output to ./venmo_output/output.txt
	
3. For unit testing, go to the designated test folder ./insight_testsuite/tests/test-plus-plus and run run_tests.sh in that folder.

## Modules

median_degree.py 
- reads the json transactions line by line from the input file
- ignores the input if actor or target is blank
- removes unicode from actor and target field and parses date string and stores transactions in tuples
- creates data structures to represent the vertex (see details below)
- imports graphcalcs.py module which defines the functions required for median degree calculation

graphcalcs.py is imported into average_degree.py. graphcalcs.py contains a function to calculate the cutoff time, by which tweets from before this time are ignored; another function calculates the average degree from the list of nodes and edges.

## Rules

To include a new line into the transaction graph:
- the entry must have at least two nodes (e.g. an actor and a target)
- the created_time must be within the 1 minute window from the maximum created_time entry

To include an entry in the sliding window:
- the created_time must be within the 1 minute window from the maximum created_time entry at each new transaction/line
- two nodes can only be connected once

## Pre-requisites

The solution has been implemented in Python 2.7

dateutil module: the parse function enables many date formats to be converted to datetime. The modules for python-dateutil-1.5 have been included in this repo ./src/dateutil - these were downloaded from https://pypi.python.org/pypi/python-dateutil/1.5.

itertools module: this module contains a set of fast, memory efficient tools. I have utilised them to remove transactions that fall out of the one minute window (compress) and to uncouple tuples into a list.
itertools documentation:
https://docs.python.org/2/library/itertools.html

Other standard python libraries included are: json, os, unittest, sys, datetime.

## Details

This solution uses data structures to build a representation of the vertex graph. These are calculated for each valid new line in the venmo-input.txt file. These data structures can be used as analysis tools, the main ones are:

degree_dict - This dictionary gives the degree of each person/node. Accessing the dictionary values gives us the degree list needed for median degree calculation.

slider_set - This gives a set of the tuples of persons. Each tuple is an edge between two nodes. Using a set dedupes the edges.

trans_list - This list of tuples gives the transaction times and the 2 persons involved in the transaction (actor and target) for the minute time window. For each new line with a valid timestamp (within 1 minute of max time), the new transaction is appended to this tuple. The tuple is truncated using itertools compress function if the time stamp no longer falls within the latest minute window. The person context (i.e. actor or target) of the person tuple is removed as not necessary for the graph (the edges are directionless).
