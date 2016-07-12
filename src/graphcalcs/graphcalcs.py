from __future__ import division

from itertools import compress
from datetime import datetime, timedelta

class GraphCalcs(object):
    """
    GraphCalcs class defines the calculations required for the vertex graph
    and median calculation.
    
    Created on: Jul 8th, 2016
    Author: Angela Razzell
    """
    
    def __init__(self):
        self.time_list = []
        self.edges_list = []
        self.nodes_list = []
        self.int_list = []
    
    def cutoff(self, time_list, delta):
        """return the minimum acceptable time for the current time window"""
        """time_list: cumulative list of created_at time"""
        """(maximum time in the list) - delta (time window of 59 seconds)"""
        return max(time_list) - timedelta(seconds=delta)
    
    def compressed_list(self, alist, ones_and_zeros):
    	"""if elem in ones_and_zeros is 0, removes corresponding elem from alist"""
    	return list(compress(alist, ones_and_zeros))
    
    def truncate_dp(self, num, n_dp):
    	"""truncates a number num to n_dp decimal places
    	(not actually necessary for median calculation of ints as always 
    	.0 or .5, but required in challenge instructions)"""
        return (int(num * 10 ** n_dp)) / 10 ** n_dp
    
    def get_median(self, int_list, n_dp):
    	"""Given a list of integers, calculates the median value.
    	get_median sorts the integers in the list, calculates the mid index(es)
    	and returns the median value from these
    	"""
        the_values = sorted(int_list)
        mid_index = len(the_values) // 2
        if len(the_values) % 2 == 1:
            return the_values[mid_index]
        else:
            upper = the_values[mid_index]
            lower = the_values[(mid_index - 1)]
            return self.truncate_dp((float(lower + upper) / 2),n_dp)

"""
if __name__ == '__main__':
    runmodule = GraphCalcs()
    runmodule.graphcalcs()
    print ('total_time: ' + str(datetime.now() - start_time))
"""