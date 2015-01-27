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
import bisect
#import pandas as pd

for n in range(1,3):
    rootdir= 'C:\\Users\\khan\\Documents\\GitHub\\AlCorrosionDataCSVFiles\\ACLData\\'
    # parameters = [port, thermocouple, length corrosion(L1), length not corrosion (L2), 
    #width corrosion (d2), width foil (d), portion pitted, pitting aspect ratio, voltage,
    #experiment type, start linear portion in hrs, stop linear portion in hrs]
    # Pitting factor: ratio of the depth of the deepest pit resulting from corrosion divided by the average 
    # penetration as calculated from weight loss. - See more at: http://www.nace.org/Pitting-Corrosion/#sthash.ATospuhX.dpuf
    if n == 1:
        # 1 Submerged expt from 10-15-14 port 1 temperature 1 1000V
        filenamelocation = rootdir+'Data_1_15_15_ACL_coupon_Al_1000V_port1.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'ACL', 0, 1, 'Data_1_15_15_ACL_coupon_Al_1000V_port1', 121]
    elif n==2:    
        # 2 Submerged expt from 10-20-14 port 1 temperature 1  100V
        filenamelocation = rootdir+'Data_ACL_1_20_15_1000V_12hrs_110C_85percenthumidity.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'ACL', 1, 2, 'Data_ACL_1_20_15_1000V_12hrs_110C_85percenthumidity', 110]
    else:
        print 'out of bounds'
    
    print n
    
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
       hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(parameters[13]-20)))*1000 #calculated resistance in m-ohms 
       
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
       hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(parameters[13]-20)))*1000 #calculated resistance in m-ohms 
     
    #print hvlist[0,:]
    #print hvlist[1,:]
     
    #N = 15
    #def runningMean(x, N):
    #    y = numpy.zeros((len(x),))
    #    for ctr in range(len(x)):
    #         y[ctr] = numpy.sum(x[ctr-N/2:(ctr+N/2)])
    #    return y/N 
        
#    lvlist[:,34] = runningMean(lvlist[:,MeasResColumn],N)
    
#    for index in range(len(lvlist[1:,34])):
#        lvlist[index,35] = ((lvlist[index,MeasResColumn]-lvlist[index-1,MeasResColumn])/(lvlist[index,20]-lvlist[index-1,20]))*1000
#    
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
    
             
    x=numpy.zeros(AverageResLen)
    y=numpy.zeros(AverageResLen)
    
    for i in range(AverageResLen):
    #    if AverageRes[i,2] >= parameters[10] and AverageRes[i,2] <= parameters[11]:
            x[i] = AverageRes[i,2]
            y[i] = AverageRes[i,1]
    
    #inds1 = indices(x, lambda x: x > parameters[10])
    #inds2 = indices(x, lambda x: x > parameters[11])
    #a1 = bisect.bisect(x, parameters[10])    
    #a2 = bisect.bisect(x, parameters[11])       
    
    regression = numpy.polyfit(x[parameters[10]:parameters[11]], y[parameters[10]:parameters[11]]*1000, 1)
    
    for i in range(AverageResLen):
        AverageRes[i,4] = AverageRes[i,2]*regression[0]+regression[1]
    
    
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 22}
    title_font = {'fontname':'Arial', 'size':'12', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
    matplotlib.rc('font', **font)
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
    #plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
    plt.plot(lvlist[:,33],lvlist[:,MeasResColumn]*1000,'ro')
    plt.plot(AverageRes[parameters[10]:parameters[11],2],AverageRes[parameters[10]:parameters[11],4], 'b', linewidth=3.0)
    #plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
    ylabel('Resistance (m-ohms)',**font)
    plt.ylim([0,150])
    #plt.xlim([0,10])
    xlabel('Time (hrs)',**font)
    title(parameters[12]+parameters[9]+'Resistance', **title_font)
    plt.legend(['Measured', 'Linear '+'y='+'%.5f' % regression[0]+'x+'+'%.5f' % regression[1]], loc='upper left')
    savefig(filenamelocation.split('_resistance_')[0]+parameters[9]+'.png')
    plt.show()
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
    
    plt.plot(AverageRes[0:AverageResLen,2],AverageRes[0:AverageResLen,3],'g')
    ylabel('Resistance Change (m-ohms/hr)',**font)
    #plt.ylim([0,5])
    #plt.xlim([0,10])
    xlabel('Time (hrs)',**font)
    title(parameters[12]+parameters[9]+'Change in Resistance', **title_font)
    #plt.legend(['Calculated', 'Measured'], loc='upper left')
    savefig(filenamelocation.split('_delRes.')[0]+parameters[9]+'ResistanceChange.png')
    plt.show()
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')   
    plt.plot(hvlist[0:-1,33],hvlist[0:-1,MeasCurColumn],'k')
    ylabel('Current (A))',**font)
    #plt.ylim([0,5])
    #plt.xlim([0,10])
    xlabel('Time (hrs)',**font)
#    title(r'Change in Calculated Resistance',**font)
    title(parameters[12]+parameters[9]+'Current', **title_font)
    #plt.legend(['Calculated', 'Measured'], loc='upper left')
    titlecurrent = filenamelocation.split
    savefig(filenamelocation.split('_delRes.')[0]+parameters[9]+'Current.png')
    plt.show()
    
    DataFile.close()