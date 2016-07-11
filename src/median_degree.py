from __future__ import division

import json
import sys
#import codecs
#import statistics

from datetime import datetime, timedelta
from dateutil.parser import parse
from itertools import chain, compress
from graphcalcs import *
from operator import itemgetter


class MedianDegree:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.graphcalcs = GraphCalcs()

    def mediandegree(self):
        
        delta = 59
        trans = {}
        time_list = []
        trans_tuple = []
        median_degree = 0.00
        people_tuple = ()
        slider_set = set()
        cutoff_time = parse("2000-01-01T00:00:01Z")
        
        with open(self.input_file,'r') as fin, \
             open(self.output_file,'w') as fout:
                
            for line in fin:
                #trans[line] = json.loads(line)
                trans = json.loads(line)
                if '' in (str(trans.get("actor")),str(trans.get("target"))):
                    continue
                
                #people_tuple = (str(trans.get("actor")),str(trans.get("target")))
                #people_tuple = sorted(people_tuple) #ignore order of the tuple
                time = parse(trans.get("created_time"))
                
                """append tuples and calculate running cutoff for time window"""
                if time >= cutoff_time:
                    people_tuple = (str(trans.get("actor")),str(trans.get("target")))
                    people_tuple = tuple(sorted(people_tuple)) #ignore order of the tuple
                    trans_tuple.append((time, (people_tuple)))
                    trans_tuple = sorted(trans_tuple, key=itemgetter(0), reverse=True)
                    time_list.append(time)
                    cutoff_time = self.graphcalcs.cutoff(time_list, delta)
                
                    """ignores entries if created_time time < cutoff time"""
                    """appends the rest of the hashtags to a list"""
                    #hashtags_slider = []
                    #initialize list of 0s to length of transaction tuple
                    valid_window = [0]*len(trans_tuple)
                    #print(len_tuple)
                    for i,(t,(act,tar)) in enumerate(trans_tuple):
                        if t >= cutoff_time:
                        	#hashtags_slider.append((act,tar))
                        	valid_window[i] = 1
                        else:
                        	#valid_window.append(0)
                        	break
                    
                    trans_tuple = list(compress(trans_tuple, valid_window))
                    hashtags_slider = list(zip(*trans_tuple))[1]
                    #each tuple is an edge between two nodes. set() dedupes the edges
                    slider_set = set(hashtags_slider) 
                    merged = list(chain(*slider_set)) #use itertools to uncouple the tuples into a list
                    d = {x:merged.count(x) for x in merged} #dictionary with degree of each node
                    #a, b = d.keys(), d.values()
                    #degrees = sorted(d.values())
                #try:
                #    median_degree = statistics.median(degrees)
                #except statistics.StatisticsError:
                #	median_degree = median_degree
                #print(degrees)
                median_degree = self.graphcalcs.getMedian(d.values())

                fout.write("%.2f" % median_degree + "\n")

            #fout.write("%.2f" % (5/3) + "\n")

if __name__ == '__main__':
    runmodule = MedianDegree(sys.argv[1], sys.argv[2])
    start_time = datetime.now()
    meddegree = runmodule.mediandegree()
    print ('total_time: ' + str(datetime.now() - start_time))
