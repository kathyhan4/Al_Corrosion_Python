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
#from datetime import datetime
import time
import matplotlib.pyplot as plt
import dateutil
from pylab import *


rootdir= 'C:\\Users\\khan\\Documents\\Al Corrosion\\Al Corrosion Data DH\\'
filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_28_14_120hr.csv'
DataFile = open(filenamelocation)
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
    date1=datetime.datetime.strptime(dateandtime, "%m/%d/%Y %I:%M:%S %p")
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
   numarray[i,33] = (numarray[i,20]-numarray[0,20])/3600

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
   elif numarray[i,0] > 0 and numarray[i,1] > 0.001:
       for m in range(0,numbercolumns):
          lvlist[l,m] = numarray[i,m]
       l=l+1
          
shapehvlist = hvlist.shape
shapelvlist = lvlist.shape
  
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
L1 = 0.05 #length of corroded area in m
L2 = 0.06 #length of non-corroded area in m
h0 = 0.000037 #thickness of foil initially in m
d = 0.005 #width of foil strip in m
secondsperpoint = 60
currentcolumn = 1 #second column is current (Amps)
Temperaturecolumn = 12

#print numpy.shape(numarray)

for i in range(0,1):
   hvlist[i,21] = abs(hvlist[i,1]) # absolute value of current
   hvlist[i,22] = hvlist[i,21] * secondsperpoint # coulombs that have been transferred over the timepoint
   hvlist[i,23] = hvlist[i,22] #this will give an error so make it not do the first row somehow
   hvlist[i,24] = hvlist[i,23] * ElecCoulomb # number of electrons transferred total, cummulative over time
   hvlist[i,25] = hvlist[i,24] / OxidationState # number of aluminum atoms removed from cathode
   hvlist[i,26] = hvlist[i,25] / NA # moles of aluminum atoms removed
   hvlist[i,27] = hvlist[i,26] * MWAl # mass of aluminum removed
   hvlist[i,28] = hvlist[i,27] / densityAl #volume of aluminum removed
   hvlist[i,29] = hvlist[i,28] / (L1*100)/(d*100)/100 # thickness of aluminum lost in m
   hvlist[i,30] = h0 - hvlist[i,29] #remaining foil thickness in m
   hvlist[i,31] = rhoAl * (L1/hvlist[i,30]/d+L2/h0/d) # ohms calculated before temperature considered
   hvlist[i,32] = (hvlist[i,31] *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
   
for i in range(1,len(hvlist)-1):
   hvlist[i,21] = abs(hvlist[i,1]) # absolute value of current
   hvlist[i,22] = hvlist[i,21] * secondsperpoint # coulombs that have been transferred over the timepoint
   hvlist[i,23] = hvlist[i-1,23] + hvlist[i,22] #this will give an error so make it not do the first row somehow
   hvlist[i,24] = hvlist[i,23] * ElecCoulomb # number of electrons transferred total, cummulative over time
   hvlist[i,25] = hvlist[i,24] / OxidationState # number of aluminum atoms removed from cathode
   hvlist[i,26] = hvlist[i,25] / NA # moles of aluminum atoms removed
   hvlist[i,27] = hvlist[i,26] * MWAl # mass of aluminum removed
   hvlist[i,28] = hvlist[i,27] / densityAl #volume of aluminum removed
   hvlist[i,29] = hvlist[i,28] / (L1*100)/(d*100)/100 # thickness of aluminum lost in m
   hvlist[i,30] = h0 - hvlist[i,29] #remaining foil thickness in m
   hvlist[i,31] = rhoAl * (L1/hvlist[i,30]/d+L2/h0/d) # ohms calculated before temperature considered
   hvlist[i,32] = (hvlist[i,31] *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
#print hvlist[0,:]
#print hvlist[1,:]

hvlistcropped_length = []
for i in range(0,len(hvlist_length)):
    x = hvlist[i,32]
    if hvlist[i,32] < 250.0:
        hvlistcropped_length.append(hvlist[i,32])
            
hvlistcropped = numpy.zeros((len(hvlistcropped_length),numbercolumns)) 
for i in range(0,len(hvlistcropped_length)):
    for j in range(0,numbercolumns):
        if hvlist[i,32] < 300.0:
            hvlistcropped [i,j] = hvlist[i,j]

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
plt.plot(hvlistcropped[:,33],hvlistcropped[:,32])
plt.plot(lvlist[:,33],lvlist[:,2]*1000,'ro')
ylabel('Resistance (m-ohms)',**font)
xlabel('Time (hrs)',**font)
title(r'Calculated Resistance',**font)
plt.legend(['Calculated', 'Measured'], loc='upper left')
savefig(filenamelocation.split('.')[0]+'.png')
plt.show()

DataFile.close()