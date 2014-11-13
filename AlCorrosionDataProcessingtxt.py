# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 16:36:15 2014

@author: khan
"""



# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 13:05:30 2014

@author: khan
"""
import csv
import os
from numpy import array
import numpy

rootdir= 'C:\\Users\\khan\\Documents\\Al Corrosion\\Al Corrosion Data DH\\'

DataFile = open(rootdir+'Data_1A_100V_with_temp1_10_24_14_120hr.txt')
#reader = csv.reader(DataFile)
#data = numpy.recfromcsv(DataFile, delimiter='\t', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')

data = numpy.loadtxt(DataFile,dtype=(numpy.string_,numpy.string_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_,numpy.float_))
#for row in reader:
# print row
# break
emptyList = []
arrayOut2 = []

size=len(data[0])
print size
print data[1]
print len(data)
numarray = numpy.zeros((len(data),size-2))

#### Parse date into second and put in list ####

for i in range(len(data)):
   x = data[i]
   for j in range(len(x)-2):
      #print j, i, len(x)
      numarray[i,j] = x[j+2]
print numarray.shape
print numarray

timearray = []

for i in range(len(data)-1):

    for j in range(1):
        x = data[i,j]
        timearray[i,0] = x[i,0] + ' ' + x[i,1]
        
print timearray    
#data = numpy.array(data)
#data_array=numpy.array(data.tolist())

# numpy.array to make a list an array then can do math with it

#Initialize variables
TimeSecondsAll = array([])
Temp1All = []
CurrentAll = []
ResistanceAll = []
VoltageAll = []
DateAll = []
TimeAll = []
DateTimeHV = []
DateTimeLV = []
CurrentHV = []
ResistanceLV = []
Temp1LV = []
Temp1HV = []
Rcalc = []


# Set constants
alphaAl = 4.29e-3 #Change of resistance with temperature in degC^-1
rhoAl = 2.65E-08 #ohm-m at 20 degC
MWAl = 26.98 #g/mol
densityAl = 2.7 #g/cc
NA = 6.022e23 #per mole
ElecCoulomb = 6.24150965e18 # electrons per coulomb
SecMinute = 60 #seconds per minute
SecHour = 3600 #seconds per hour

#Set Inputs Specific to this Run
VoltageBias = -1000 #V
OxidationState = 2 #electrons per Al atom in reaction
L1 = 5 #length of corroded area in cm
L2 = 6 #length of non-corroded area in cm
h0 = 0.0037 #thickness of foil initially in cm
d = 0.5 #width of foil strip in cm

DataFile.close()