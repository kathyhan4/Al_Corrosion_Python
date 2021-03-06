# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 13:05:30 2014

@author: khan
"""


import csv
import os
from numpy import array
import numpy
import datetime
from datetime import datetime
import time



rootdir= 'C:\\Users\\khan\\Documents\\Al Corrosion\\Al Corrosion Data DH\\'

DataFile = open(rootdir+'Data_1A_100V_with_temp1_10_24_14_120hr.csv')
data = numpy.recfromcsv(DataFile, delimiter='\t', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')


size2=len(data[0])
numbercolumns = size2 + 13
print size2
print data[1]
print len(data)
numarray = numpy.zeros((len(data),numbercolumns)) 

timearray = []

for i in range(len(data)):
    date = data[i][0]
    time2 = data[i][1]
    dateandtime = date + ' ' +  time2
    date1=datetime.strptime(dateandtime, "%m/%d/%Y %I:%M:%S %p")
    date2 = time.mktime(date1.timetuple())
    timearray.append(date2)

#### Parse date into second and put in list ####
for i in range(len(data)):
   x = data[i]
   for j in range(len(x)-2):
      numarray[i,j] = x[j+2]
      
print numarray.shape

for i in range(len(timearray)):
   numarray[i,20] = timearray[i]

shapenumarray = numarray.shape

hvlist_length = []
lvlist_length = []

for i in range(0,len(timearray)):
    x = numarray[i]
    if numarray[i,0] < -50.0:
        hvlist_length.append(x)
    elif numarray[i,0]>0:
        lvlist_length.append(x)

hvlist = numpy.zeros((len(hvlist_length),numbercolumns))
lvlist = numpy.zeros((len(lvlist_length),numbercolumns))

k=0
l=0

for i in range(0,len(timearray)):
   if numarray[i,0] < -50.0:
       for j in range(0,numbercolumns):
          hvlist[k,j] =numarray[i,j]
       k=k+1
   elif numarray[i,0]>0:
       for j in range(0,numbercolumns):
          lvlist[l][j] = numarray[l][j]
       l+l+1
          
shapehvlist = hvlist.shape
shapelvlist = lvlist.shape
  
#for i in range(shapehvlist[0]):
#   x = hvlist[i]
#   for j in range(len(x)):
#      #print j, i, len(x)
#      hvlist2[i,j] = float(hvlist[i,j])    
#print hvlist 
#print lvlist 


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
secondsperpoint = 60
currentcolumn = 1 #second column is current (Amps)
Temperaturecolumn = 12

#print numpy.shape(numarray)

for i in range(0,1):
   hvlist[i,21] = abs(hvlist[i,1]) # absolute value of current
   hvlist[i,22] = hvlist[i,1] * secondsperpoint # coulombs that have been transferred over the timepoint
   hvlist[i,23] = hvlist[i,22] #this will give an error so make it not do the first row somehow
   hvlist[i,24] = hvlist[i,23] * ElecCoulomb # number of electrons transferred total, cummulative over time
   hvlist[i,25] = hvlist[i,24] / OxidationState # number of aluminum atoms removed from cathode
   hvlist[i,26] = hvlist[i,25] / NA # moles of aluminum atoms removed
   hvlist[i,27] = hvlist[i,26] * MWAl # mass of aluminum removed
   hvlist[i,28] = hvlist[i,27] / densityAl #volume of aluminum removed
   hvlist[i,29] = hvlist[i,28] / L1/100/d/100 # thickness of aluminum lost
   hvlist[i,30] = h0 - hvlist[i,29]/100
   hvlist[i,31] = rhoAl * (L1/hvlist[i,30]/d+L2/h0/d)
   hvlist[i,32] = (hvlist[i,31] *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
   
for i in range(1,len(hvlist)-1):
   hvlist[i,21] = abs(hvlist[i,1]) # absolute value of current
   hvlist[i,22] = hvlist[i,1] * secondsperpoint # coulombs that have been transferred over the timepoint
   hvlist[i,23] = hvlist[i-1,23] + numarray[i,22] #this will give an error so make it not do the first row somehow
   hvlist[i,24] = hvlist[i,23] * ElecCoulomb # number of electrons transferred total, cummulative over time
   hvlist[i,25] = hvlist[i,24] / OxidationState # number of aluminum atoms removed from cathode
   hvlist[i,26] = hvlist[i,25] / NA # moles of aluminum atoms removed
   hvlist[i,27] = hvlist[i,26] * MWAl # mass of aluminum removed
   hvlist[i,28] = hvlist[i,27] / densityAl #volume of aluminum removed
   hvlist[i,29] = hvlist[i,28] / L1/100/d/100 # thickness of aluminum lost
   hvlist[i,30] = h0 - hvlist[i,29]/100
   hvlist[i,31] = rhoAl * (L1/hvlist[i,30]/d+L2/h0/d)
   hvlist[i,32] = (hvlist[i,31] *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
print hvlist[1,:]
DataFile.close()