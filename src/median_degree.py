"""
MedianDegree class 
- reads the input file with json transactions from venmo
- stores data structures for the transactions at each line
- stores a sliding window (list) of transactions within the one minute window...
- which enables us to calculate the median degree
- writes the medians to the output file

graphcalcs module is imported for calculated functions
    
Created on: Jul 8th, 2016
Author: Angela Razzell
"""
	
#from __future__ import division

# generic imports:
import json
import sys

# function imports:
from datetime import datetime, timedelta
from dateutil.parser import parse
from itertools import chain
#from operator import itemgetter

# universal import for graphcalcs module:
from graphcalcs.graphcalcs import *

class MedianDegree:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.graphcalcs = GraphCalcs()
        
    def mediandegree(self):
        
        delta = 59 # for 1 minute time window
        trans = {}
        time_list = []
        trans_list = []
        median_degree = 0.00
        people_tuple = ()
        slider_set = set()
        cutoff_time = parse("2000-01-01T00:00:01Z") # set to generic past date so file will read first line
        
        with open(self.input_file,'r') as fin, \
             open(self.output_file,'w') as fout:
            
            for line in fin:
                trans = json.loads(line)
                
                # ignore this input (if actor or target is empty):
                # use str() to remove unicode
                if '' in (str(trans.get("actor")),str(trans.get("target"))):
                    continue
                
                #dateutil parse function to read date
                time = parse(trans.get("created_time"))
                # if line contains timestamp outside of 1 min window
                # then median_degree remains as per previous line / 
                # no need to recalculate.
                if time < cutoff_time:
                    median_degree = median_degree
                    continue
                
                #append tuples and calculate running cutoff for time window
                couple = (str(trans.get("actor")),str(trans.get("target")))
                #ignore order of the tuple, helps deduping when we set the slider_set
                people_tuple = tuple(sorted(couple))
                trans_list.append((time, (people_tuple)))
                #trans_list = sorted(trans_list, key=itemgetter(0), reverse=True) #sort by time descending.
                #time_list = list(zip(*trans_list))[0] -- equals list of times 
                cutoff_time = self.graphcalcs.cutoff(list(zip(*trans_list))[0], delta)
                
                #initialize list of 0s to length of trans_list
                valid_window = [0]*len(trans_list)
                #valid_window list checks whether time in trans_list is valid 
                for i,(t,_) in enumerate(trans_list):
                    if t >= cutoff_time:
                        valid_window[i] = 1
                    else:
                        #valid_window[i] = 0
                        continue
                        
                # use itertools compress to remove transactions that are out of the 1 min window
                trans_list = self.graphcalcs.compressed_list(trans_list, valid_window)
                # list of person tuples in 1 min window
                persons_slider = list(zip(*trans_list))[1]
                #each tuple is an edge between two nodes. set() dedupes the edges
                slider_set = set(persons_slider) 
                merged = list(chain(*slider_set)) #use itertools chain to uncouple the tuples in the set into a list
                #dictionary with degree of each node
                degree_dict = {x:merged.count(x) for x in merged}
                median_degree = self.graphcalcs.get_median(degree_dict.values(),2)
                fout.write("%.2f" % median_degree + "\n")
            
if __name__ == '__main__':
    runmodule = MedianDegree(sys.argv[1], sys.argv[2])
    start_time = datetime.now()
    meddegree = runmodule.mediandegree()
    print ('total_time: ' + str(datetime.now() - start_time))
