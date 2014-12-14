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


rootdir= 'C:\\Users\\khan\\Documents\\GitHub\\AlCorrosionDataCSVFiles\\'
# parameters = [port, thermocouple, length corrosion(L1), length not corrosion (L2), width corrosion (d2), width foil (d), portion pitted, pitting aspect ratio, voltage]
# Pitting factor: ratio of the depth of the deepest pit resulting from corrosion divided by the average 
# penetration as calculated from weight loss. - See more at: http://www.nace.org/Pitting-Corrosion/#sthash.ATospuhX.dpuf

## 1 Submerged expt from 10-15-14 port 1 temperature 1 1000V
#filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_15_14_24hr_new_Al.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'Submerged']

## 2 Submerged expt from 10-20-14 port 1 temperature 1  100V
#filenamelocation = rootdir+'Data_100mA_100V_with_temp1_10_20_14_48hr.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged']

## 3 Submerged expt from 10-22-14 port 1 temperature 1  1000V
### DO NOT USE, FAT ANODE
#filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_22_14_48hr.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'Submerged_Fat_Anode']

## 4 Submerged expt from 10-24-14 port 1 temperature 1 100V
### DO NOT USE, FAT ANODE
#filenamelocation = rootdir+'Data_1A_100V_with_temp1_10_24_14_120hr.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged_Fat_Anode']

## 5 Submerged expt from 10-27-14 port 1 temperature 1 0V
### DO NOT USE, FAT ANODE
#filenamelocation = rootdir+'Data_1A_0V_with_temp1_10_27_14_120hr_control.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, 0, 'Submerged_Fat_Anode']

## 6 Submerged expt from 10-28-14 port 1 temperature 1 1000V
#filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_28_14_120hr.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'Submerged']

## 7 Submerged expt from 10-29-14 port 1 temperature 1 500V
#filenamelocation = rootdir+'Data_1A_500V_with_temp1_10_29_14_120hr.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -500, 'Submerged']

## 8 Submerged expt from 10-31-14 port 1 temperature 1 100V
#filenamelocation = rootdir+'Data_1A_100V_with_temp1_10_31_14_120hr.csv'
#parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged']

## 9 DH expt from 11-3-14 port 1 temperature 2 1000V
#filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_3_14_480hr_DH.csv'
#parameters = [1, 2, 0.004, 0.066, 0.005, 0.005, 0.1, 1, -1000, 'DampHeat']

## 10 DH expt from 11-7-14 port 1 temperature 2 1000V
#filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon.csv'
#parameters = [1, 2, 0.004, 0.066, 0.005, 0.005, 0.1, 1, -1000, 'DampHeat']

## 11 Submerged expt from 11-10-14 port 2 temperature 1 100V and 1000V
#filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon_aqueous_in_port_2_100_and_1000V_for_imaging_11_10_14.csv'
#parameters = [2, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100]

## 12 Submerged expt from 11-20-14 port 2 temperature 1 1000V Cu strip, tinned
#filenamelocation = rootdir+'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14.csv'
#parameters = [2, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'Submerged']

## 13 Submerged expt from 11-20-14 port 3 temperature 3 100V 
#filenamelocation = rootdir+'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14.csv'
#parameters = [3, 3, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged']

## 14 DH expt from 11-20-14 port 1 temperature 2 1000V
#filenamelocation = rootdir+'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14.csv'
#parameters = [1, 2, 0.004, 0.066, 0.005, 0.005, 0.1, 1, -1000, 'DampHeat']

## 14 DH expt from 11-7-14 port 1 temperature 2 1000V
#filenamelocation = rootdir+'Data_DH_Port1_1000V_Temp2_maybe_more_P2_P3_11-26-14.csv'
#parameters = [1, 2, 0.004, 0.066, 0.005, 0.005, 0.1, 1, -1000, 'DampHeat']



DataFile = open(filenamelocation)
data = numpy.recfromcsv(DataFile, delimiter='\t', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')


size2=len(data[0])
numbercolumns = size2 + 15
Port = parameters[0]
Thermocouple = parameters[1]
currentcolumn = Port * 3 - 2 #second column for that port's data is current (Amps)
Temperaturecolumn = Thermocouple + 11
MeasResColumn = Port * 3 - 1
MeasCurColumn = Port * 3 - 2
MeasVoltColumn = Port * 3 - 3

#Set Inputs Specific to this Run
VoltageBias = parameters[8] #V
Current4Wire = 1 #1 amp in 4 wire measurement
OxidationState = 3 #electrons per Al atom in reaction
L1 = parameters[2] #length of corroded area in m
L2 = parameters[3] #length of non-corroded area in m
h0 = 0.000037 #thickness of foil initially in m
d = parameters[5] #width of foil strip in m
secondsperpoint = 60

Area1 = 0.15 # Portion of the length of L1 that has deep pitting
Area2 = 0.4 # Portion of length L1 that has medium pitting
Area3 = 0.45 # Portion of area with mild corrosion
Portion1 = 0.5 # percent of aluminum removal in area 1
Portion2 = 0.25 # percent of aluminum rmoval in area 2
Portion3 = 0.25 # percent of aluminum rmoval in area 3

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
    if numarray[i,MeasVoltColumn] < VoltageBias/2:
        hvlist_length.append(x)

    elif numarray[i,MeasCurColumn] > Current4Wire/2:
#    elif numarray[i,MeasVoltColumn] > 0 and numarray[i,MeasCurColumn] > Current4Wire/2:
        lvlist_length.append(x)

hvlist = numpy.zeros((len(hvlist_length),numbercolumns))
lvlist = numpy.zeros((len(lvlist_length),numbercolumns))

k=0
l=0


for i in range(0,len(timearray)):
   if numarray[i,MeasVoltColumn] < VoltageBias/2:
       for j in range(0,numbercolumns):
          hvlist[k,j] =numarray[i,j]
       k=k+1
   elif numarray[i,MeasCurColumn] > Current4Wire/2:
       for m in range(0,numbercolumns):
          lvlist[l,m] = numarray[i,m]
       l=l+1

for i in range(len(lvlist)-1):
   lvlist[i,21] = lvlist[i,20] - lvlist[i-1,20] # difference in time points
   
lvlist[0,21] = 1
   
Rsum = 0
Rsumlength = 0
timethreshold = 360
Restime = 0
AverageRes = numpy.zeros((len(lvlist_length),numbercolumns))
counter1 = 0

for i in range(0,len(lvlist)-1):
    Rsum = Rsum + lvlist[i,MeasResColumn]
    Rsumlength = Rsumlength + 1
    Restime = Restime + lvlist[i,20]
    if lvlist[i,21] > timethreshold:
        AverageRes[counter1,1] = Rsum / Rsumlength
        AverageRes[counter1,0] = Restime / Rsumlength
        Rsum = 0
        Rsumlength = 0
        Restime = 0
        counter1 = counter1 + 1
        
for i in range(1,len(AverageRes[:,0])-1):
    AverageRes[i,2] = (AverageRes[i,0] - AverageRes[0,0])/3600
    AverageRes[i,3] = ((AverageRes[i,1] - AverageRes[i-1,1])/(AverageRes[i,2] - AverageRes[i-1,2]))*1000

AverageResLen = 0

for i in range(1,len(AverageRes[:,0])-1):
    if AverageRes[i,2] > 0:
        AverageResLen = AverageResLen + 1
   
         
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



#print numpy.shape(numarray)

for i in range(0,1):
   hvlist[i,21] = abs(hvlist[i,4]) # absolute value of current
   hvlist[i,22] = hvlist[i,21] * secondsperpoint # coulombs that have been transferred over the timepoint
   hvlist[i,23] = hvlist[i,22] #this will give an error so make it not do the first row somehow
   hvlist[i,24] = hvlist[i,23] * ElecCoulomb # number of electrons transferred total, cummulative over time
   hvlist[i,25] = hvlist[i,24] / OxidationState # number of aluminum atoms removed from cathode
   hvlist[i,26] = hvlist[i,25] / NA # moles of aluminum atoms removed
   hvlist[i,27] = hvlist[i,26] * MWAl # mass of aluminum removed
   hvlist[i,28] = hvlist[i,27] / densityAl #volume of aluminum removed in cc
   hvlist[i,29] = h0 - 0.01*(hvlist[i,28]*Portion1/(d*100*L1*100*Area1)) # remaining thickness in m in area1
   hvlist[i,30] = h0 - 0.01*(hvlist[i,28]*Portion2/(d*100*L1*100*Area2)) # remaining thickness in m in area2
   hvlist[i,31] = h0 - 0.01*(hvlist[i,28]*Portion3/(d*100*L1*100*Area3)) # remaining thickness in m in area3
   hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
   
for i in range(1,len(hvlist)-1):
   hvlist[i,21] = abs(hvlist[i,4]) # absolute value of current
   hvlist[i,22] = hvlist[i,21] * (hvlist[i,20]-hvlist[i-1,20]) # coulombs that have been transferred over the timepoint
   hvlist[i,23] = hvlist[i-1,23] + hvlist[i,22] #this will give an error so make it not do the first row somehow
   hvlist[i,24] = hvlist[i,23] * ElecCoulomb # number of electrons transferred total, cummulative over time
   hvlist[i,25] = hvlist[i,24] / OxidationState # number of aluminum atoms removed from cathode
   hvlist[i,26] = hvlist[i,25] / NA # moles of aluminum atoms removed
   hvlist[i,27] = hvlist[i,26] * MWAl # mass of aluminum removed
   hvlist[i,28] = hvlist[i,27] / densityAl #volume of aluminum removed
   hvlist[i,29] = h0 - 0.01*(hvlist[i,28]*Portion1/(d*100*L1*100*Area1)) # remaining thickness in m in area1
   hvlist[i,30] = h0 - 0.01*(hvlist[i,28]*Portion2/(d*100*L1*100*Area2)) # remaining thickness in m in area2
   hvlist[i,31] = h0 - 0.01*(hvlist[i,28]*Portion3/(d*100*L1*100*Area3)) # remaining thickness in m in area3
   hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
 
#print hvlist[0,:]
#print hvlist[1,:]
 
N = 15
def runningMean(x, N):
    y = numpy.zeros((len(x),))
    for ctr in range(len(x)):
         y[ctr] = numpy.sum(x[ctr-N/2:(ctr+N/2)])
    return y/N 
    
lvlist[:,34] = runningMean(lvlist[:,MeasResColumn],N)

for index in range(len(lvlist[1:,34])):
    lvlist[index,35] = ((lvlist[index,MeasResColumn]-lvlist[index-1,MeasResColumn])/(lvlist[index,20]-lvlist[index-1,20]))*1000

hvlistcropped_length = []
for i in range(0,len(hvlist_length)):
    x = hvlist[i,32]
    if hvlist[i,32] < 75.0:
        hvlistcropped_length.append(hvlist[i,32])
            
hvlistcropped = numpy.zeros((len(hvlistcropped_length),numbercolumns)) 
for i in range(0,len(hvlistcropped_length)):
    for j in range(0,numbercolumns):
        if hvlist[i,32] < 75.0:
            hvlistcropped [i,j] = hvlist[i,j]

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
plt.plot(lvlist[:,33],lvlist[:,MeasResColumn]*1000,'ro')
#plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
ylabel('Resistance (m-ohms)',**font)
plt.ylim([0,100])
#plt.xlim([0,10])
xlabel('Time (hrs)',**font)
title(r'Calculated Resistance',**font)
plt.legend(['Calculated', 'Measured'], loc='upper left')
savefig(filenamelocation.split('_resistance_')[0]+parameters[9]+'.png')
plt.show()

figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')

plt.plot(AverageRes[0:AverageResLen,2],AverageRes[0:AverageResLen,3],'g')
ylabel('Resistance Change (m-ohms/hr)',**font)
#plt.ylim([0,5])
#plt.xlim([0,10])
xlabel('Time (hrs)',**font)
title(r'Change in Calculated Resistance',**font)
#plt.legend(['Calculated', 'Measured'], loc='upper left')
savefig(filenamelocation.split('_delRes.')[0]+parameters[9]+'ResistanceChange.png')
plt.show()

DataFile.close()