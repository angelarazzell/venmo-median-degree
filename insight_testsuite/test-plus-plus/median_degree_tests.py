"""Unit tests to check functions in graphcalcs.py and output versus input of median_degree.py

Created on: Jul 8th, 2016
Author: Angela Razzell
"""

from __future__ import division
import unittest
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src/')
#sys.path.append('./src/')

from graphcalcs.graphcalcs import *
from datetime import datetime, timedelta
from dateutil.parser import parse
from median_degree import *


class CalculationsCheck(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CalculationsCheck, self).__init__(*args, **kwargs)
        #self.module_path = module_path
        self.graphcalcs = GraphCalcs()
    
    def test_truncate_dp(self):
        """test whether truncate_dp gives expected truncation after 2dp"""
        known_values = ((5/3, 1.66),(1, 1.00),(7/9, 0.77),(4.5, 4.50))
        for fract, num in known_values:
            result = self.graphcalcs.truncate_dp(num, 2)
        self.assertEqual(num, result)
    
    def test_get_median(self):
        """tests whether get_median function is working as expected"""
        lists = [[1,1,1],[1,2,3],[1,2,3,4],[5,7,2],[1,2,3,4,5,6,7,8,9,10,11,12,13]]
        known_medians = [1.00, 2.00, 2.50, 5.00, 7.00]
        for i,alist in enumerate(lists):
            result = self.graphcalcs.get_median(alist,2)
        self.assertEqual(known_medians[i], result)
    
    def test_cutoff(self):
        """tests whether cutoff function is working as expected for simple example"""
        expected = parse("2016-08-07T00:48:57Z")
        time_list = [parse("2016-05-16T15:45:01Z"),parse("2016-08-07T00:49:56Z"),parse("2014-10-31T07:22:44Z"),parse("2015-12-24T09:03:24Z")]
        result = self.graphcalcs.cutoff(time_list, 59)
        self.assertEqual(expected, result)
    
    def test_compressed_list(self):
        """tests whether compressed_list function is working as expected for simple example"""
        degree_list  = [1,4,5,6,5,16,20,2]
        ones_n_zeros = [1,0,0,1,1,1,0,1]
        expected = [1,6,5,16,2]
        result = self.graphcalcs.compressed_list(degree_list,ones_n_zeros)
        self.assertEqual(expected, result)

class TestIO(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIO, self).__init__(*args, **kwargs)
        #self.module_path = module_path
        self.file_dir = os.path.dirname(os.path.realpath(__file__))
        self.runmodule = MedianDegree(self.file_dir+ '/venmo-trans_actor_blank.txt' \
        	, self.file_dir + '/venmo-output_actor_blank.txt')
        self.median_degree = self.runmodule.mediandegree()
    
    #def run_median_degree(self):
    #	return self.median_degree
    	
    def test_line_nums(self):
    	"""checks input and output file line numbers are as expected 
    	also checks whether the blank actor (or target) field is removed correctly"""
        with open(self.file_dir + '/venmo-trans_actor_blank.txt') as fin, \
          open(self.file_dir + '/venmo-output_actor_blank.txt') as fout:
            input_lines = len(fin.readlines())
            output_lines = len(fout.readlines())
            expected_lines = input_lines - 3 #there are 3 blank actors in test input
            #for line in fin:
            #    trans = json.loads(line)
            #    if '' == str(trans.get("actor")):
            #        expected_lines = input_lines - 1
            self.assertEqual(expected_lines, output_lines)
     
if __name__ == '__main__':
    unittest.main()
    