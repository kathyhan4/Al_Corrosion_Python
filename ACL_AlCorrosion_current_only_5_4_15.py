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

#initiate list for storing total joules in each linear portion for each experiment
Current_slope_output = numpy.zeros((100,15))

for n in range(51,52):
    rootdir= 'C:\\Users\\khan\\Documents\\GitHub\\AlCorrosionDataCSVFiles\\ACLData\\'
    # parameters = [0 port, 1 thermocouple, 2 length corrosion(L1), 3 length not corrosion (L2), 
    #4 width corrosion (d2), 5 width foil (d), 6 portion pitted, 7 pitting aspect ratio, 8 voltage,
    #9 experiment type, 10 start linear portion in hrs, 11 stop linear portion in hrs], 12 file name, 
    #13 temperature of experiment, 14 AverageRes start row for calculating foil thickness remaining
    
    # Pitting factor: ratio of the depth of the deepest pit resulting from corrosion divided by the average 
    # penetration as calculated from weight loss. - See more at: http://www.nace.org/Pitting-Corrosion/#sthash.ATospuhX.dpuf
    if n == 1:
        # 1 ACL port 1 1000V Al coupon from 1-15-15
        filenamelocation = rootdir+'Data_1_15_15_ACL_coupon_Al_1000V_port1.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'ACL', 0, 1, 'Data_1_15_15_ACL_coupon_Al_1000V_port1', 121, 0]
    elif n==32:    
        # 32 111 Coupons for testing leakage current 5mm cathode 3/4 inch anode no bubble 85/85 5/1/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_smallan_without_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '5 mm cathode 0.75 inch anode no bubble', 1000, 9000, 'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_smallan_without_defect', 85, 1]
    elif n==33:    
        # 33 112 Coupons for testing leakage current 5mm cathode 3/4 inch anode with bubble 85/85 5/4/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_smallan_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '5 mm cathode 0.75 inch anode with bubble', 1000, 2800, 'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_smallan_with_defect', 85, 1]
    elif n==34:    
        # 33 231 Coupons for testing leakage current 19 mm cathode 151 mm anode  no bubble 85/85 5/5/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_medcat_largean_without_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '19 mm cathode 150 mm anode no bubble', 100, 1050, 'Data_85_85_port2addr25bottom_currentmeasurement_medcat_largean_without_defect', 85, 1]
    elif n==35:    
        # 35 222 Coupons for testing leakage current 19 mm cathode 51 mm anode with bubble 85/85 5/6/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_medcat_medan_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '19 mm cathode 51 mm anode with bubble', 300, 2700, 'Data_85_85_port2addr25bottom_currentmeasurement_medcat_medan_with_defect', 85, 1]
    elif n==36:    
        # 36 322 Coupons for testing leakage current 51 mm cathode 51 mm anode with bubble 85/85 5/7/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_largecat_medan_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '51 mm cathode 51 mm anode with bubble', 400, 3300, 'Data_85_85_port2addr25bottom_currentmeasurement_largecat_medan_with_defect', 85, 1]
    elif n==37:    
        # 37 212 Coupons for testing leakage current 19 mm cathode 19 mm anode with bubble 85/85 5/8/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_medcat_smallan_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '19 mm cathode 19 mm anode with bubble', 300, 2700, 'Data_85_85_port2addr25bottom_currentmeasurement_medcat_smallan_with_defect', 85, 1]
    elif n==38:    
        # 38 331 Coupons for testing leakage current 51 mm cathode 151 mm anode no bubble 85/85  *must re-do*!
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_largecat_largean_no_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '19 mm cathode 151 mm anode no bubble', 300, 2800, 'Data_85_85_port2addr25bottom_currentmeasurement_largecat_largean_no_defect', 85, 1]
    elif n==39:    
        # 39 122 Coupons for testing leakage current 5 mm cathode 51 mm anode with bubble 85/85 5/11/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_medan_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '5 mm cathode 51 mm anode with bubble', 300, 3000, 'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_medan_with_defect', 85, 1]
    elif n==40:    
        # 40 311 Coupons for testing leakage current 51 mm cathode 19 mm anode with bubble 85/85 5/12/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_largecat_smallan_no_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '51 mm cathode 19 mm anode no bubble', 300, 3000, 'Data_85_85_port2addr25bottom_currentmeasurement_largecat_smallan_no_defect', 85, 1]
    elif n==41:    
        # 41 312 Coupons for testing leakage current 19 mm cathode 51 mm anode with bubble 85/85 5/13/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_largecat_smallan_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '51 mm cathode 19 mm anode with bubble', 300, 3000, 'Data_85_85_port2addr25bottom_currentmeasurement_largecat_smallan_with_defect', 85, 1]
    elif n==42:    
        # 42 121 Coupons for testing leakage current 5 mm cathode 51 mm anode no bubble 85/85 5/14/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_medan_no_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '5 mm cathode 51 mm anode no bubble', 300, 3000, 'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_medan_no_defect', 85, 1]
    elif n==43:    
        # 43 321 Coupons for testing leakage current 51 mm cathode 51 mm anode no bubble 85/85 5/17/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_largecat_medan_no_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '51 mm cathode 51 mm anode no bubble', 300, 3000, 'Data_85_85_port2addr25bottom_currentmeasurement_largecat_medan_no_defect', 85, 1]
    elif n==44:    
        # 44 232 Coupons for testing leakage current 19 mm cathode 151 mm anode with bubble 85/85 5/18/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_medcat_largean_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '19 mm cathode 151 mm anode with bubble', 200, 1800, 'Data_85_85_port2addr25bottom_currentmeasurement_medcat_largean_with_defect', 85, 1]
    elif n==45:    
        # 45 132 Coupons for testing leakage current 5 mm cathode 151 mm anode with bubble 85/85  5/19/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_largean_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '5 mm cathode 151 mm anode with bubble', 300, 2500, 'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_largean_with_defect', 85, 1]
    elif n==46:    
        # 46 211 Coupons for testing leakage current 19 mm cathode 19 mm anode no bubble 85/85 5/20/15
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_medcat_smallan_no_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '19 mm cathode 19 mm anode no bubble', 400, 2400, 'Data_85_85_port2addr25bottom_currentmeasurement_medcat_smallan_no_defect', 85, 1]
    elif n==47:    
        # 47 221 Coupons for testing leakage current 19 mm cathode 51 mm anode no bubble 85/85 
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_medcat_medan_no_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '19 mm cathode 51 mm anode no bubble', 300, 2000, 'Data_85_85_port2addr25bottom_currentmeasurement_medcat_medan_no_defect', 85, 1]
    elif n==48:    
        # 48 332 Coupons for testing leakage current 51 mm cathode 151 mm anode with bubble 85/85 
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_largecat_largean_with_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '51 mm cathode 151 mm anode with bubble', 300, 2000, 'Data_85_85_port2addr25bottom_currentmeasurement_largecat_largean_with_defect', 85, 1]
    elif n==49:    
        # 49 131 Coupons for testing leakage current 5 mm cathode 151 mm anode no bubble 85/85 
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_largean_no_defect.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '5 mm cathode 151 mm anode no bubble', 300, 2000, 'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_largean_no_defect', 85, 1]
    elif n==50:    
        # 50 5 mm cathode 19 mm anode with defect also with cosmetic tape 85/85 5/15/15 
        filenamelocation = rootdir+'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_smallan_with_defect_with_cosmetic_tape.csv'
        parameters = [2, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, '5 mm cathode 151 mm anode no bubble', 400, 4000, 'Data_85_85_port2addr25bottom_currentmeasurement_smallcat_smallan_with_defect_with_cosmetic_tape', 85, 1]
    elif n==51:    
        # 51 gen E Cu cell coupon, shorted as cathode 19 mm anode square in center of cell (Si side, glass) without defect 85/85 7/13/15  port 1 DH7
        filenamelocation = rootdir+'DH7_port1_leakagecurrent_7-13-15.csv'
        parameters = [1, 2, .05, 0.066, .005, 0.005, 0.1, 1, 1000, 'Cu cell coupon leakage center 19x19mm', 400, 1000, 'DH7_port1_leakagecurrent_7-13-15', 85, 1]

#notice that in this file parameters[10] and parameters[11] are the start and stop line numbers for the current average


# parameters = [0 port, 1 thermocouple, 2 length corrosion(L1), 3 length not corrosion (L2), 
    #4 width corrosion (d2), 5 width foil (d), 6 portion pitted, 7 pitting aspect ratio, 8 voltage,
    #9 experiment type, 10 start linear portion in hrs, 11 stop linear portion in hrs], 12 file name, 
    #13 temperature of experiment, 14 AverageRes start row for calculating foil thickness remaining
    else:
        print 'out of bounds'
    
    print n
    
    DataFile = open(filenamelocation)
    data = numpy.recfromcsv(DataFile, delimiter='\t', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')
    
    
    size2=len(data[0])
    numbercolumns = size2 + 16
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
    alpha = 0.00429 #Change in Resistivity per degree C
    
        # Set constants
    alphaAl = 4.29e-3 #Change of resistance with temperature in degC^-1
    rhoAl = 2.65E-08 #ohm-m at 20 degC
    MWAl = 26.98 #g/mol
    densityAl = 2.7 #g/cc
    NA = 6.022e23 #per mole
    ElecCoulomb = 6.24150965e18 # electrons per coulomb
    SecMinute = 60 #seconds per minute
    SecHour = 3600 #seconds per hour
    
    
#    Area1 = 0.15 # Portion of the length of L1 that has deep pitting
#    Area2 = 0.4 # Portion of length L1 that has medium pitting
#    Area3 = 0.45 # Portion of area with mild corrosion
#    Portion1 = 0.5 # percent of aluminum removal in area 1
#    Portion2 = 0.25 # percent of aluminum rmoval in area 2
#    Portion3 = 0.25 # percent of aluminum rmoval in area 3
    
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
        if abs(numarray[i,MeasVoltColumn]) > abs(VoltageBias/2):
            hvlist_length.append(x)
    
        elif numarray[i,MeasCurColumn] > Current4Wire/2:
    #    elif numarray[i,MeasVoltColumn] > 0 and numarray[i,MeasCurColumn] > Current4Wire/2:
            lvlist_length.append(x)
    
    hvlist = numpy.zeros((len(hvlist_length),numbercolumns))
    lvlist = numpy.zeros((len(lvlist_length),numbercolumns))
    
    k=0
    l=0
    
    
    for i in range(0,len(timearray)):
       if abs(numarray[i,MeasVoltColumn]) > abs(VoltageBias/2):
           for j in range(0,numbercolumns):
              hvlist[k,j] =numarray[i,j]
           k=k+1
       elif numarray[i,MeasCurColumn] > Current4Wire/2:
           for m in range(0,numbercolumns):
              lvlist[l,m] = numarray[i,m]
           l=l+1
    
#    for i in range(len(lvlist)-1):
#       lvlist[i,21] = lvlist[i,20] - lvlist[i-1,20] # difference in time points
#       lvlist[i,36] = lvlist[i,MeasResColumn]*parameters[4]/((1+alpha*(parameters[13]-20))*parameters[2])
       
#    lvlist[0,21] = 1
       
#    Rsum = 0
#    Rsum2 = 0
#    Rsumlength = 0
#    timethreshold = 60
#    timethreshold = 360
#    Restime = 0
##    AverageRes = numpy.zeros((len(lvlist_length),numbercolumns))
#    AverageResSeed = numpy.zeros((40*parameters[11],numbercolumns))
#    AverageRes = numpy.zeros((10*parameters[11],numbercolumns))
#    counter1 = 0
# 
##   group and average resistance measurements
#    for i in range(0,len(lvlist)-1):
#        Rsum = Rsum + lvlist[i,MeasResColumn]
#        Rsum2 = Rsum2 + lvlist[i,36] #to average R*w/L/temp adjust
#        Rsumlength = Rsumlength + 1
#        Restime = Restime + lvlist[i,20]
#        if lvlist[i,21] > timethreshold: #for large gaps in time, report the average of the last batch of resistances
#            AverageResSeed[counter1,1] = Rsum / Rsumlength
#            AverageResSeed[counter1,0] = Restime / Rsumlength
#            AverageResSeed[counter1,5] = Rsum2 / Rsumlength
#            AverageResSeed[counter1,8] = parameters[13]
#            AverageResSeed[counter1,9] = AverageResSeed[counter1,1]/(1+alpha*(AverageResSeed[counter1,8]-20))            
#            Rsum = 0
#            Rsum2 = 0
#            Rsumlength = 0
#            Restime = 0
#            counter1 = counter1 + 1
            

    
#    for i in range(len(data)):
#        date = data[i][0]
#        time2 = data[i][1]
#        dateandtime = date + ' ' +  time2
#        date1=datetime.datetime.strptime(dateandtime, "%m/%d/%Y %I:%M:%S %p")
#        date2 = time.mktime(date1.timetuple())
#        timearray.append(date2)
        
#    for i in range(1,len(AverageRes[:,0])-1):
#        AverageResSeed[i,2] = (AverageResSeed[i,0] - AverageResSeed[0,0])/3600 #time in hours since start
#        AverageResSeed[i,3] = ((AverageResSeed[i,1] - AverageResSeed[i-1,1])/(AverageResSeed[i,2] - AverageResSeed[i-1,2]))*1000 #change in m-ohm per hour
#        AverageResSeed[i,6] = ((AverageResSeed[i,5] - AverageResSeed[i-1,5])/(AverageResSeed[i,2] - AverageResSeed[i-1,2]))*1000 #change adjusted for temp and corrosion area
#
#    vectorx = numpy.zeros(12)  
#    counter2 = 0 
#    
#    for i in range(0,len(AverageResSeed[:,0])-1):
#        if AverageResSeed[i,3] < 10 and AverageResSeed[i,3] > 0:
#            AverageRes[counter2,:] = AverageResSeed[i,:]
#            counter2 = counter2+1
#            
#    AverageRes[parameters[14],10] = 0.000037 #um of initial foil thickness
#    
#    for i in range(parameters[14]+1,len(AverageRes[:,0])-1):
#        AverageRes[i,10] = 1/(((AverageRes[i,1]-AverageRes[i-1,1])*parameters[4]/rhoAl/parameters[2])+1/AverageRes[i-1,10])
#        AverageRes[i,11] = (AverageRes[i,10]-AverageRes[i-1,10])/(AverageRes[i,2]-AverageRes[i-1,2])*1000000
#        
#    AverageResLen = 0
#    
#    for i in range(1,len(AverageRes[:,0])-1):
#        if AverageRes[i,2] > 0:
#            AverageResLen = AverageResLen + 1
       
             
    shapehvlist = hvlist.shape
    shapelvlist = lvlist.shape
      

    
    
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
#       hvlist[i,29] = h0 - 0.01*(hvlist[i,28]*Portion1/(d*100*L1*100*Area1)) # remaining thickness in m in area1
#       hvlist[i,30] = h0 - 0.01*(hvlist[i,28]*Portion2/(d*100*L1*100*Area2)) # remaining thickness in m in area2
#       hvlist[i,31] = h0 - 0.01*(hvlist[i,28]*Portion3/(d*100*L1*100*Area3)) # remaining thickness in m in area3
#       hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(parameters[13]-20)))*1000 #calculated resistance in m-ohms 
       
    for i in range(1,len(hvlist)-1):
       hvlist[i,21] = abs(hvlist[i,4]) # absolute value of current
       hvlist[i,22] = hvlist[i,21] * (hvlist[i,20]-hvlist[i-1,20]) # coulombs that have been transferred over the timepoint
       hvlist[i,23] = hvlist[i-1,23] + hvlist[i,22] #this will give an error so make it not do the first row somehow
       hvlist[i,24] = hvlist[i,23] * ElecCoulomb # number of electrons transferred total, cummulative over time
       hvlist[i,25] = hvlist[i,24] / OxidationState # number of aluminum atoms removed from cathode
       hvlist[i,26] = hvlist[i,25] / NA # moles of aluminum atoms removed
       hvlist[i,27] = hvlist[i,26] * MWAl # mass of aluminum removed
       hvlist[i,28] = hvlist[i,27] / densityAl #volume of aluminum removed
#       hvlist[i,29] = h0 - 0.01*(hvlist[i,28]*Portion1/(d*100*L1*100*Area1)) # remaining thickness in m in area1
#       hvlist[i,30] = h0 - 0.01*(hvlist[i,28]*Portion2/(d*100*L1*100*Area2)) # remaining thickness in m in area2
#       hvlist[i,31] = h0 - 0.01*(hvlist[i,28]*Portion3/(d*100*L1*100*Area3)) # remaining thickness in m in area3
#       hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(parameters[13]-20)))*1000 #calculated resistance in m-ohms 
#     
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
    
             
#    x=numpy.zeros(AverageResLen) #initiate vector to store times for regression
#    y=numpy.zeros(AverageResLen) # initiate vector to store average resistances for regression
#    y2 = numpy.zeros(AverageResLen)# for regression of R*w/L/temp adjust
#    y3 = numpy.zeros(AverageResLen)# for regression of R*w/L/temp adjust    
#    
#    for i in range(AverageResLen):
#    #    if AverageRes[i,2] >= parameters[10] and AverageRes[i,2] <= parameters[11]:
#            x[i] = AverageRes[i,2]
#            y[i] = AverageRes[i,1]
#            y2[i] = AverageRes[i,5]
#            y3[i] = AverageRes[i,10]
#    
#    #inds1 = indices(x, lambda x: x > parameters[10])
#    #inds2 = indices(x, lambda x: x > parameters[11])
#    #a1 = bisect.bisect(x, parameters[10])    
#    #a2 = bisect.bisect(x, parameters[11])       
#    
#    regression = numpy.polyfit(x[parameters[10]:parameters[11]], y[parameters[10]:parameters[11]]*1000, 1)
#    regression2 = numpy.polyfit(x[parameters[10]:parameters[11]], y2[parameters[10]:parameters[11]]*1000, 1)
#    regression3 = numpy.polyfit(x[parameters[10]:parameters[11]], y3[parameters[10]:parameters[11]], 1)
    
#    for i in range(AverageResLen):
#        AverageRes[i,4] = AverageRes[i,2]*regression[0]+regression[1]
#        AverageRes[i,7] = AverageRes[i,2]*regression2[0]+regression2[1]
#        AverageRes[i,12] = AverageRes[i,2]*regression3[0]+regression3[1]


        
#    Add up current over time to get total joules per time point
#        Then sum up the column (34) to get cummulative joules
    hvlinestart = 0
    hvlinestop = 0
#    hvlinestart = [s for s, i in enumerate(hvlistcropped[:,33]) if i>AverageRes[parameters[10],2]][0]
#    hvlinestop  = [s for s, i in enumerate(hvlistcropped[:,33]) if i>AverageRes[parameters[11]-1,2]][0]

    for i in range(0,len(hvlist_length)-1):
       hvlist[i,34] = (hvlist[i,33]-hvlist[i-1,33])*3600*hvlist[i,currentcolumn]
       hvlist[i,35] = hvlist[i,currentcolumn]
#       column 34 represents the number of seconds in the past time point times the current, which is equal to joules
    totaljoules = []
    totaljoules = numpy.sum(hvlist[:,34])
    Current_slope_output[n,0] = parameters[10]
    Current_slope_output[n,1] = parameters[11]
#    totaljoulesall[n,2] = totaljoules/(parameters[11]-parameters[10])
#    totaljoulesall[n,3] = sum(hvlist[:,34])/(hvlinestop-hvlinestart)
    Current_slope_output[n,4] = (sum(abs(hvlist[parameters[10]:parameters[11],currentcolumn])))/(parameters[11]-parameters[10])*1e9 #average current in nA over times of interest
#    Current_slope_output[n,5] = regression[0]
#    Current_slope_output[n,6] = regression2[0]    
#    Current_slope_output[n,7] = sum(AverageRes[parameters[10]:parameters[11],11])/(parameters[11]-parameters[10])
#    Current_slope_output[n,8] = AverageResLen
#    Current_slope_output[n,9] = regression3[0]*1000000
#    Current_slope_output[n,10] = regression3[1]*1000000
    
    totaljoules = 0
    
    
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 22}
    title_font = {'fontname':'Arial', 'size':'12', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
    matplotlib.rc('font', **font)
    
#    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
#    #plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
#    plt.plot(lvlist[:,33],lvlist[:,MeasResColumn]*1000,'ro')
#    plt.plot(AverageRes[parameters[10]:parameters[11],2],AverageRes[parameters[10]:parameters[11],4], 'b', linewidth=3.0)
#    plt.plot(hvlist[0:-1,33],hvlist[0:-1,34]*(-100), 'g', linewidth=3.0)
#    #plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
#    ylabel('Resistance (m-ohms)',**font)
#    plt.ylim([10,30])
#    #plt.xlim([0,10])
#    xlabel('Time (hrs)',**font)
#    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance', **title_font)
#    plt.legend(['Measured', 'Linear '+'y='+'%.5f' % regression[0]+'x+'+'%.5f' % regression[1]], loc='upper left')
##    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
#    savefig(rootdir+'Resistance\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Resistance.png')
#
#    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
#    #plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
##    plt.plot(AverageRes[parameters[14]:AverageResLen-1,2],AverageRes[parameters[14]:AverageResLen-1,1]*1000,'ro') ADD ME BACK IN LATER 4-22-15
##    plt.plot(AverageRes[parameters[14]:AverageResLen-1,2],AverageRes[parameters[14]:AverageResLen-1,9]*1000, 'g', linewidth=3.0)
#    plt.plot(AverageRes[parameters[14]:AverageResLen-1,2],AverageRes[parameters[14]:AverageResLen-1,10]*1000000, 'ko', linewidth=3.0)
#    plt.plot(AverageRes[parameters[10]:parameters[11],2],AverageRes[parameters[10]:parameters[11],12]*1000000, 'k', linewidth=3.0)
##    plt.plot(hvlist[0:-1,33],hvlist[0:-1,34]*(-20), 'g', linewidth=3.0)
#    #plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
#    ylabel('Adjusted (temp) Resistance (m-ohms) and Remaining Al Thickness (um)',**font)
#    plt.ylim([32,40])
#    plt.xlim([20,90])
#    xlabel('Time (hrs)',**font)
#    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance_Adjusted_temperature', **title_font)
##    plt.legend(['Measured Resistance','Remaining Thickness Calculated (um)', 'Remaining Thickness Regression (um)'], loc='upper left') ADD ME BACK IN LATER 4-22-15
##    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
#    savefig(rootdir+'Adjusted Resistance\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Resistance_adjusted_temp_area.png')


#    plt.show()
    
    
#    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')   
#    plt.plot(hvlist[0:-1,33],hvlist[0:-1,Temperaturecolumn],'b')
##    plt.plot(hvlist[0:-1,33],abs(hvlist[0:-1,MeasCurColumn]),'k')
#    ylabel('Temperature (C))',**font)
##    plt.yscale('log')
#    #plt.ylim([0,5])
##    plt.xlim([0,5])
#    xlabel('Time (hrs)',**font)
##    title(r'Change in Calculated Resistance',**font)
#    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Temperature', **title_font)
#    #plt.legend(['Calculated', 'Measured'], loc='upper left')
#    titlecurrent = filenamelocation.split
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'Temperature.png')
#    plt.show()
    
    
#    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
#    plt.plot(AverageRes[0:AverageResLen,2],AverageRes[0:AverageResLen,3],'g')
#    ylabel('Resistance Change (m-ohms/hr)',**font)
#    #plt.ylim([0,5])
#    #plt.xlim([0,10])
#    xlabel('Time (hrs)',**font)
#    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Change in Resistance', **title_font)
#    #plt.legend(['Calculated', 'Measured'], loc='upper left')
##    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'ResistanceChange.png')
#    savefig(rootdir+'Resistance Change\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Resistance_Change.png')

#    plt.show()
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')   
    plt.plot(hvlist[0:-1,33],abs(hvlist[0:-1,MeasCurColumn])*1e9,'k')
#    plt.plot(hvlist[0:-1,33],abs(hvlist[0:-1,MeasCurColumn]),'k')
    ylabel('Current (nA))',**font)
#    plt.yscale('log')
#    plt.ylim([-1,2])
#    plt.xlim([0,0.3])
    xlabel('Time (hrs)',**font)
#    plt.xlim([0,90])
#    title(r'Change in Calculated Resistance',**font)
    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Leakage Current Expt', **title_font)
    #plt.legend(['Calculated', 'Measured'], loc='upper left')
    titlecurrent = filenamelocation.split
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'Current.png')
    savefig(rootdir+'Current\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'LeakageCurrentExpt.png')

#    plt.show()
    
DataFile.close()
timestamp = time.time()
first_time_seconds = str(math.floor(timestamp))    
numpy.savetxt('C:\\Users\\khan\\Documents\\GitHub\\AlCorrosionDataCSVFiles\\ACLData\\OutputDataFiles\\'+first_time_seconds+'_'+str(i)+'.txt',Current_slope_output)


#    elif n==2:    
#        # 2 ACL port 1 1000V Al coupon from 1-20-15
#        filenamelocation = rootdir+'Data_ACL_1_20_15_1000V_12hrs_110C_85percenthumidity.csv'
#        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'ACL', 3, 6, 'Data_ACL_1_20_15_1000V_12hrs_110C_85percenthumidity', 110, 2]
#    elif n==3:    
#        # 3 ACL port 1 1000V Al coupon from 1-22-15
#        filenamelocation = rootdir+'Data_ACL_1_22_15_1000V_8and4hrs_110C_85percenthumidity.csv'
#        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'ACL', 0, 1, 'Data_ACL_1_22_15_1000V_8and4hrs_110C_85percenthumidity', 110, 0]
#    elif n==4:    
#        # 4 ACL port 1 1000V Al coupon from 1-23-15
#        filenamelocation = rootdir+'Data_ACL_1_23_15_1000V_60hrs_110C_85percenthumidity.csv'
#        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'ACL', 0, 1, 'Data_ACL_1_23_15_1000V_60hrs_110C_85percenthumidity', 110, 0]
#    elif n==5:    
#        # 5 ACL port 1 100V Al coupon from 1-27-15
#        filenamelocation = rootdir+'Data_ACL_1_27_15_100V_60hrs_110C_85percenthumidity.csv'
#        parameters = [1, 1, 0.0033, 0.03, 0.005, 0.005, 0.5, 1, -100, 'ACL', 32, 37, 'Data_ACL_1_27_15_100V_60hrs_110C_85percenthumidity', 110, 0]
#    elif n==6:    
#        # 6 ACL port 1 100V Al coupon from 1-27-15
#        filenamelocation = rootdir+'Data_ACL_1_27_15_100V_60hrs_110C_85percenthumidity_cropped.csv'
#        parameters = [1, 1, 0.0033, 0.03, 0.005, 0.005, 0.5, 1, -100, 'ACL', 2, 21, 'Data_ACL_1_27_15_100V_60hrs_110C_85percenthumidity_cropped', 110, 2]
#    elif n==7:    
#        # 7 ACL port 1 100V Al coupon from 2-2-15
#        filenamelocation = rootdir+'Data_ACL_2_2_15_100V_96hrs_121C_100percenthumidity.csv'
#        parameters = [1, 1, 0.0027, 0.03, 0.0051, 0.005, 0.5, 1, -100, 'ACL', 20, 40, 'Data_ACL_2_2_15_100V_96hrs_121C_100percenthumidity', 121, 2]
#    elif n==8:    
#        # 8 ACL port 1 1000V Al coupon from 2-11-15
#        filenamelocation = rootdir+'Data_ACL_2_11_15_1000V_96hrs_121C_100percenthumidityport1.csv'
#        parameters = [1, 1, 0.0034, 0.03, 0.0049, 0.005, 0.5, 1, -1000, 'ACL', 29, 75, 'Data_ACL_2_11_15_1000V_96hrs_121C_100percenthumidityport1', 121, 2]
#    elif n==9:    
#        # 9 ACL port 1 200V Al coupon from 2-9-15
#        filenamelocation = rootdir+'Data_ACL_2_9_15_200V_44hrs_121C_100percenthumidityport1.csv'
#        parameters = [1, 1, 0.0037, 0.03, 0.0044, 0.005, 0.5, 1, -200, 'ACL', 33, 44, 'Data_ACL_2_9_15_200V_44hrs_121C_100percenthumidityport1', 121, 2]
#    elif n==10:    
#        # 10 ACL port 1 100V Al coupon from 2-6-15
#        filenamelocation = rootdir+'Data_ACL_2_6_15_100V_60hrs_121C_100percenthumidityport1_port2BareAl_0V.csv'
#        parameters = [1, 1, 0.0024, 0.03, 0.0049, 0.005, 0.5, 1, -100, 'ACL', 4, 58, 'Data_ACL_2_6_15_100V_60hrs_121C_100percenthumidityport1_port2BareAl_0V', 121, 2]
#    elif n==11:    
#        # 11 ACL port 1 100V Al coupon from 2-17-15
#        filenamelocation = rootdir+'Data_ACL_2_17_15_1000V_121C_100percenthumidityport1_same_sample_12_hr_121_85.csv'
#        parameters = [1, 1, 0.0033, 0.03, 0.0049, 0.005, 0.5, 1, -100, 'ACL', 8, 16, 'Data_ACL_2_17_15_1000V_121C_100percenthumidityport1_same_sample_12_hr_121_85', 121, 2]
#    elif n==12:    
#        # 12 ACL port 1 300V Al coupon from 2-23-15
#        filenamelocation = rootdir+'Data_ACL_2_23_15_300V_110C_92percenthumidityport1_combined.csv'
#        parameters = [1, 1, 0.004, 0.03, 0.005, 0.005, 0.5, 1, -300, 'ACL', 0, 1, 'Data_ACL_2_23_15_300V_110C_92percenthumidityport1_combined', 110, 0]
#    elif n==13:    
#        # 13 ACL port 1 1000V Al coupon from 2-27-15 121 C 60% humidity
#        filenamelocation = rootdir+'Data_ACL_2_27_15_1000V_121C_60percenthumidityport1.csv'
#        parameters = [1, 1, 0.0033, 0.03, 0.0049, 0.005, 0.5, 1, -1000, 'ACL', 50, 68, 'Data_ACL_2_27_15_1000V_121C_60percenthumidityport1', 121, 2]
#    elif n==14:    
#        # 14 ACL port 1 100V Al coupon from 3-3-15 121 C 85% humidity
#        filenamelocation = rootdir+'Data_ACL_3_3_15_Port1_100V_Port2_1000V_121C_85percenthumidity.csv'
#        parameters = [1, 1, 0.0033, 0.03, 0.0049, 0.005, 0.5, 1, -100, 'ACL', 90, 108, 'Data_ACL_3_3_15_Port1_100V_Port2_1000V_121C_85percenthumidity', 121, 2]
#    elif n==15:    
#        # 15 ACL port 2 1000V Al coupon from 3-3-15 121 C 85% humidity
#        filenamelocation = rootdir+'Data_ACL_3_3_15_Port1_100V_Port2_1000V_121C_85percenthumidity.csv'
#        parameters = [2, 1, 0.0033, 0.03, 0.0049, 0.005, 0.5, 1, -1000, 'ACL', 50, 78, 'Data_ACL_3_3_15_Port1_100V_Port2_1000V_121C_85percenthumidity', 121, 1]
#    elif n==16:    
#        # 16 ACL port 2 1000V Al coupon from 3-10-15 121 C 85% humidity
#        filenamelocation = rootdir+'Data_ACL_3_10_15b_Port1_1000V_Port2_100V_121C_85percenthumidity.csv'
#        parameters = [2, 1, 0.0033, 0.003, 0.0049, 0.005, 0.5, 1, -1000, 'ACL -1000V', 3, 65, 'Data_ACL_3_10_15b_Port1_1000V_Port2_100V_121C_85percenthumidity', 121, 2]
#    elif n==17:    
#        # 17 DH port 1 1000V Al low resistance coupon from 3-16-15 65 C 50% humidity
#        filenamelocation = rootdir+'Data_DH_port1_65_65_1000V_port2_85_85_1000V_3_16_15_combined.csv'
#        parameters = [1, 1, 0.0043, 0.0032, 0.0047, 0.005, 0.5, 1, -1000, 'DH 65_50_-1000V', 3, 290, 'Data_DH_port1_65_65_1000V_port2_85_85_1000V_3_16_15_combined', 65, 2]
#    elif n==18:    
#        # 18 DH port 2 1000V Al coupon from 3-16-15 85 C 50% humidity
#        filenamelocation = rootdir+'Data_DH_port1_65_65_1000V_port2_85_85_1000V_3_16_15-85_combined.csv'
#        parameters = [2, 1, 0.00266, 0.00437, 0.00437, 0.005, 0.5, 1, -1000, 'DH 85_50_-1000V', 47, 92, 'Data_DH_port1_65_65_1000V_port2_85_85_1000V_3_16_15-85_combined', 85, 2]
#    elif n==19:    
#        # 19 DH port 2 1000V Al coupon from 3-27-15 85 C 50% humidity
#        filenamelocation = rootdir+'Data_DH_1000V_port2_85_50_1000V_3-27-15.csv'
#        parameters = [2, 1, 0.00266, 0.00437, 0.00437, 0.005, 0.5, 1, -1000, 'DH 85_50_-1000V', 18, 31, 'Data_DH_1000V_port2_85_50_1000V_3-27-15', 85, 2]
#    elif n==20:    
#        # 20 DH port 3 100V Al coupon from 3-27-15 85 C 50% humidity
#        filenamelocation = rootdir+'Data_DH_100V_port3_85_50_100V_3-27-15.csv'
#        parameters = [3, 1, 0.00266, 0.00437, 0.00437, 0.005, 0.5, 1, -100, 'DH 85_50_-1000V', 2, 10, 'Data_DH_1000V_port2_85_85_1000V_3-25-15', 85, 2]
#    elif n==21:    
#        # DH port 1 65/50 -1000V
#        filenamelocation = rootdir+'March31Testing3.csv'
#        parameters = [1, 1, 0.00266, 0.00437, 0.00437, 0.005, 0.5, 1, -1000, 'March31Testing3Port1', 1, 2, 'March31Testing', 65, 1]
#    elif n==22:    
#        # DH port 2 85/50 -1000V
#        filenamelocation = rootdir+'March31Testing3.csv'
#        parameters = [2, 1, 0.00266, 0.00437, 0.00437, 0.005, 0.5, 1, -1000, 'March31Testing3Port2', 1, 2, 'March31Testing', 85, 1]
#    elif n==23:    
#        # DH port 2 85/50 -100V
#        filenamelocation = rootdir+'March31Testing3.csv'
#        parameters = [3, 1, 0.00266, 0.00437, 0.00437, 0.005, 0.5, 1, -100, 'March31Testing3Port3', 1, 2, 'March31Testing', 85, 1]
#    elif n==24:    
#        # 24 Damp Heat Al coupon 60/85 from 2/2/15 edited to exclude bad readings
#        filenamelocation = rootdir+'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined_edited.csv'
#        parameters = [2, 2, 0.0033, 0.003, 0.0049, 0.005, 0.1, 1, -1000, 'DH_60_85', 10, 520, 'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined_edited', 60, 5]
#    elif n==25:    
#        # 25 Damp Heat Al low resistance coupon 65/50 from 3/16/15  port 1
#        filenamelocation = rootdir+'Data_DH_port1_#25_65_50_1000V_3_16_15_combined.csv'
#        parameters = [1, 2, 0.0043, 0.08, 0.00323, 0.00474, 0.1, 1, -1000, 'DH_65_50', 50, 75, 'Data_DH_port1_#25_65_50_1000V_3_16_15_combined', 65, 10]
#    elif n==26:    
#        # 26 Damp Heat Al coupon 85/50 from 3/27/15 -1000V port 2
#        filenamelocation = rootdir+'Data_DH_port2_#26_85_50_1000V_port3_#27_85_50_1000V_3_27_15_combined.csv'
#        parameters = [2, 2, 0.00205, 0.08, 0.0045, 0.0045, 0.1, 1, -1000, 'DH_85_50', 4, 50, 'Data_DH_port2_#26_85_50_1000V_port3_#27_85_50_1000V_3_27_15_combined', 85, 3]
#    elif n==27:    
#        # 27 Damp Heat Al coupon 85/50 from 3/27/15 -1000V port 3
#        filenamelocation = rootdir+'Data_DH_port2_#26_85_50_1000V_port3_#27_85_50_1000V_3_27_15_combined.csv'
#        parameters = [3, 2, 0.0025, 0.08, 0.00475, 0.00475, 0.1, 1, -1000, 'DH_85_50', 25, 50, 'Data_DH_port2_#26_85_50_1000V_port3_#27_85_50_1000V_3_27_15_combined', 85, 3]
#    elif n==28:    
#        # 28 Damp Heat Al bubble on back coupon 85/85 from 4/1/15 port 1
#        filenamelocation = rootdir+'Data_85_85_port1_backsidebubble_port2_normalfrontside_4_1_15.csv'
#        parameters = [1, 2, 0.0154, 0.08, 0.00465, 0.00465, 0.1, 1, -1000, 'DH_85_85_backsidebubble', 11, 44, 'Data_85_85_port1_backsidebubble_port2_normalfrontside_4_1_15', 85, 11]
#    elif n==29:    
#        # 29 Damp Heat Al coupon 85/85 from 4/1/15 port 2
#        filenamelocation = rootdir+'Data_85_85_port1_backsidebubble_port2_normalfrontside_4_1_15.csv'
#        parameters = [2, 2, 0.003, 0.08, 0.0048, 0.0048, 0.1, 1, -1000, 'DH_85_85', 11, 70, 'Data_85_85_port1_backsidebubble_port2_normalfrontside_4_1_15', 85, 11]
#    elif n==30:    
#        # 18 DH expt from 12-18-14 port 1 temperature 2 1000V Al no bubble
#        filenamelocation = rootdir+'DH_12_18_14_to_1_23_15_1AlNoBubble_2AlPrimered_3tinnedCu_nobubble.csv'
#        parameters = [1, 2, .05, 0.066, .005, 0.005, 0.1, 1, -1000, 'DampHeatNoBubble', 4, 38, 'DH_12_18_14_to_1_23_15_1AlNoBubble_2AlPrimered_3tinnedCu', 85, 3]
#    elif n==31:    
#        # 31 Submerged switching polarities
#        filenamelocation = rootdir+'#31_Data_Sub_Port3_SwitchingPolarities_4-7-15.csv'
#        parameters = [3, 2, .05, 0.066, .005, 0.005, 0.1, 1, -1000, 'Submerged_Switching_Polarities', 0, 2, '#31_Data_Sub_Port3_SwitchingPolarities_4-7-15', 25, 1]
