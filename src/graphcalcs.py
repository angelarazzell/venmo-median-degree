#from __future__ import division
from datetime import datetime, timedelta

class GraphCalcs:

    def __init__(self):
        self.time_list = []
        self.edges_list = []
        self.nodes_list = []
        self.numericValues = []

        
    def cutoff(self, time_list, delta):
        """return the minimum acceptable time for the current time window"""
        """time_list: cumulative list of created_at time"""
        """(maximum time in the list) - delta (time window of 59 seconds)"""
        return max(time_list) - timedelta(seconds=delta)

    def degreecalc(self, edges_list, nodes_list):
        """returns the average degree of a vertex in a Twitter hashtag graph"""
        noedges = len(set(edges_list))
        nonodes = len(set(nodes_list))
        try: 
            return (noedges / nonodes)
        except ZeroDivisionError:
            return (noedges / 1)
    
    def getMedian(self, numericValues):
        theValues = sorted(numericValues)
        if len(theValues) % 2 == 1:
            return theValues[((len(theValues)+1)//2)-1]
        else:
            lower = theValues[(len(theValues)//2)-1]
            upper = theValues[len(theValues)//2]
            return (float(lower + upper)) / 2
    
    """
    def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])
    """