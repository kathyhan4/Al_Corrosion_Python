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

DataFile = open(rootdir+'Data_1A_100V_with_temp1_10_24_14_120hr.csv')
#reader = csv.reader(DataFile)
data = numpy.recfromcsv(DataFile, delimiter='\t', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')
#for row in reader:
#    print row
#    break
#data = numpy.array(data)
data_array=numpy.array(data.tolist())
print data
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

#Process Data
for filename in os.listdir(top):
    if filename.endswith("csv"):
        f = open(top + '\\' + filename, 'r')
        datafile = csv.reader(f)
        header = f.readline() #readline automatically reads only the first line
        
        for lines in datafile:
            if lines[1] == "PrePower":
                PrePower.append(float(lines[2]))
            if lines[1] == "PostPower":
                PostPower.append(float(lines[2]))
        f.close()
        
        #Calculate dPower and write the result to a summary file
        for i in range(len(PrePower)):
            dPower.append((PostPower[i]-PrePower[i])/PrePower[i]*100)
            sf.write(str(PrePower[i]) + ',' + str(PostPower[i]) + ',' + str(dPower[i]) + '\n')
        
sf.close()