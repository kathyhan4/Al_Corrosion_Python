# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 12:45:17 2014

@author: khan
"""
import csv
import os
from numpy import array
import numpy

rootdir= 'C:\\Users\\khan\\Documents\\Al Corrosion\\Al Corrosion Data DH\\'

input_file = rootdir+'Data_1A_100V_with_temp1_10_24_14_120hr.csv'
for line in open(input_file):
   line_split = line.split("\t")
#   for item in line_split:
#      print item
#   print "end of line
print line_split