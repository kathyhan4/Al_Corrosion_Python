# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 13:05:30 2014

@author: khan
"""
# This program is intended for use with 37 um thick aluminum foil

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
Current_slope_output = numpy.zeros((100,10))

for n in range(18,19):
#    for the range the first number should be the first experiment you want to analyze, the second is one number higher than the last.
#   Example: if you want to analyze experiments # 16 through 20, type range(16,21)
    rootdir= 'C:\\Users\\khan\\Documents\\GitHub\\AlCorrosionDataCSVFiles\\Submerged and DH\\'
    # parameters = [0 port, 1 thermocouple, 2 length corrosion(L1), 3 length not corrosion (L2), 
    #4 width corrosion (d2), 5 width foil (d), 6 portion pitted, 7 pitting aspect ratio, 8 voltage,
    #9 experiment type, 10 start linear portion in hrs, 11 stop linear portion in hrs], 12 file name, 
    #13 temperature of experiment, 14 AverageRes start row for calculating foil thickness remaining
    # Pitting factor: ratio of the depth of the deepest pit resulting from corrosion divided by the average 
    # penetration as calculated from weight loss. - See more at: http://www.nace.org/Pitting-Corrosion/#sthash.ATospuhX.dpuf
    if n == 1:
        # 1 Submerged expt from 10-15-14 port 1 temperature 1 1000V
        filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_15_14_24hr_new_Al.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'Submerged', 6, 17, 'Data_1A_1000V_with_temp1_10_15_14_24hr_new_Al', 'placeholder', 1]
    elif n==2:    
        # 2 Submerged expt from 10-20-14 port 1 temperature 1  100V
        filenamelocation = rootdir+'Data_100mA_100V_with_temp1_10_20_14_48hr.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged', 19, 44, 'Data_100mA_100V_with_temp1_10_20_14_48hr', 'placeholder', 1]
    elif n==3:    
        # 3 Submerged expt from 10-22-14 port 1 temperature 1  1000V
        ## DO NOT USE, FAT ANODE
        filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_22_14_48hr.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'Submerged_Fat_Anode', 2, 5, 'Data_1A_1000V_with_temp1_10_22_14_48hr', 'placeholder', 1]
    elif n==4:    
        # 4 Submerged expt from 10-24-14 port 1 temperature 1 100V
        ## DO NOT USE, FAT ANODE
        filenamelocation = rootdir+'Data_1A_100V_with_temp1_10_24_14_120hr.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged_Fat_Anode', 10, 45, 'Data_1A_100V_with_temp1_10_24_14_120hr', 'placeholder', 1]
#    elif n==5:    
#        # 5 Submerged expt from 10-27-14 port 1 temperature 1 0V
#        ## DO NOT USE, FAT ANODE
#        filenamelocation = rootdir+'Data_1A_0V_with_temp1_10_27_14_120hr_control.csv'
#        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, 0, 'Submerged_Fat_Anode', 5, 10]
    elif n==6:    
        # 6 Submerged expt from 10-28-14 port 1 temperature 1 1000V
        filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_28_14_120hr.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'Submerged', 6, 14, 'Data_1A_1000V_with_temp1_10_28_14_120hr', 'placeholder', 1]
    elif n==7:    
        # 7 Submerged expt from 10-29-14 port 1 temperature 1 500V
        filenamelocation = rootdir+'Data_1A_500V_with_temp1_10_29_14_120hr.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -500, 'Submerged', 15, 46, 'Data_1A_500V_with_temp1_10_29_14_120hr', 'placeholder', 1]
    elif n==8:   
        # 8 Submerged expt from 10-31-14 port 1 temperature 1 100V
        filenamelocation = rootdir+'Data_1A_100V_with_temp1_10_31_14_120hr.csv'
        parameters = [1, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged', 25, 67, 'Data_1A_100V_with_temp1_10_31_14_120hr', 'placeholder', 1]
    elif n==9:   
        # 9 DH expt from 11-3-14 port 1 temperature 2 1000V
        filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_3_14_480hr_DH.csv'
        parameters = [1, 2, 0.005, 0.066, 0.004, 0.005, 0.1, 1, -1000, 'DampHeat', 30, 46, 'Data_1A_1000V_with_temp2_11_3_14_480hr_DH', 'placeholder', 1]
    elif n==10:    
        # 10 DH expt from 11-7-14 port 1 temperature 2 1000V
        filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon.csv'
        parameters = [1, 2, 0.004, 0.066, 0.003, 0.005, 0.1, 1, -1000, 'DampHeat', 20, 60, 'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon', 'placeholder', 1]
    elif n==11:    
        # 11 Submerged expt from 11-10-14 port 2 temperature 1 100V and 1000V
        filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon_aqueous_in_port_2_100_and_1000V_for_imaging_11_10_14.csv'
        parameters = [2, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'Submerged', 40, 55, 'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon_aqueous_in_port_2_100_and_1000V_for_imaging_11_10_14', 'placeholder', 1]
    elif n==12:    
        # 12 Submerged expt from 11-20-14 port 2 temperature 1 1000V Cu strip, tinned
        filenamelocation = rootdir+'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14.csv'
        parameters = [2, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'SubmergedCu', 1, 120, 'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14', 'placeholder', 1]
    elif n==13:    
        # 13 Submerged expt from 11-20-14 port 3 temperature 3 100V 
        filenamelocation = rootdir+'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14.csv'
        parameters = [3, 3, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -100, 'SubmergedAl', 15, 27, 'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14', 'placeholder', 1]
    elif n==14:    
        # 14 DH expt from 11-20-14 port 1 temperature 2 1000V
        filenamelocation = rootdir+'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14.csv'
        parameters = [1, 2, 0.0033, 0.003, 0.00475, 0.005, 0.1, 1, -1000, 'DampHeat', 5, 130, 'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage_from_11_20_14', 'placeholder', 1]
    elif n==15:    
        # 15 DH expt from 11-26-14 port 1 temperature 2 1000V
        filenamelocation = rootdir+'Data_DH_Port1_1000V_Temp2_maybe_more_P2_P3_11-26-14.csv'
        parameters = [1, 2, 0.004, 0.066, 0.003, 0.005, 0.1, 1, -1000, 'DampHeat', 5, 130, 'Data_DH_Port1_1000V_Temp2_maybe_more_P2_P3_11-26-14', 'placeholder', 1]
    elif n==16:    
        # 16 Submerged gray painted Al 12-10-14 port 2 temperature 1 1000V
        filenamelocation = rootdir+'Data_graypainted_port2_temp1_1000V_submerged_12_10_through_12_15b.csv'
        parameters = [2, 1, 0.05, 0.06, 0.005, 0.005, 0.5, 1, -1000, 'SubmergedGrayPaintedAl', 20, 70, 'Data_graypainted_port2_temp1_1000V_submerged_12_10_through_12_15b', 'placeholder', 1]
    elif n==17:    
        # 17 DH expt from 12-12-14 port 1 temperature 2 1000V
        filenamelocation = rootdir+'Data_DH_from 12-12-14_Port1_1000V_Temp2.csv'
        parameters = [1, 2, 0.004, 0.066, 0.005, 0.005, 0.1, 1, -1000, 'DampHeat', 30, 45, 'Data_DH_from 12-12-14_Port1_1000V_Temp2', 'placeholder', 1]
    elif n==18:    
        # 18 DH expt from 12-18-14 port 1 temperature 2 1000V Al no bubble
        filenamelocation = rootdir+'DH_12_18_14_to_1_23_15_1AlNoBubble_2AlPrimered_3tinnedCu_nobubble.csv'
        parameters = [1, 2, .05, 0.066, .005, 0.005, 0.1, 1, -1000, 'DampHeatNoBubble', 700, 800, 'DH_12_18_14_to_1_23_15_1AlNoBubble_2AlPrimered_3tinnedCu', 'placeholder', 1]
    elif n==19:    
        # 19 DH expt from 12-18-14 port 2 temperature 2 1000V Al primeered with grey VHT primer
        filenamelocation = rootdir+'DH_PrimerAlCoupon_12_18_14_to_1_9_15port2.csv'
        parameters = [2, 2, 0.003, 0.066, 0.003, 0.005, 0.1, 1, -1000, 'DampHeatVHTPrimerAl', 325, 490, 'DH_PrimerAlCoupon_12_18_14_to_1_9_15port2', 'placeholder', 1]
    elif n==20:    
        # 20 DH expt from 12-18-14 port 3 temperature 2 1000V Tinned Copper coupon
        filenamelocation = rootdir+'DH_12_18_14_to_1_23_15_1AlNoBubble_2AlPrimered_3tinnedCu.csv'
        parameters = [3, 2, 0.001, 0.066, 0.001, 0.005, 0.1, 1, -1000, 'DampHeatTinnedCu', 100, 800, 'DH_12_18_14_to_1_23_15_1AlNoBubble_2AlPrimered_3tinnedCu', 'placeholder', 1]
    elif n==21:    
        # 21 Submerged expt from 1-14-15 port 2 temperature 1 1000V Al-Cu strip I SUSPECT THIS EXXPERIMENT RAN OUT OF WATER AND DID NOT CORRODE PROPERLY
        filenamelocation = rootdir+'Data_DH_from 12-18-14_Port1_NoBubbleCoupon_Port3_tinnedCu_allDHCoupons1000V_restarted_1_14_15b.csv'
        parameters = [2, 1, 0.05, 0.066, 0.001, 0.005, 0.1, 1, -1000, 'SubmergedCuAlBad', 9, 20, 'Data_DH_from 12-18-14_Port1_NoBubbleCoupon_Port3_tinnedCu_allDHCoupons1000V_restarted_1_14_15b', 'placeholder', 1]
    elif n==22:    
        # 22 Submerged expt from 2-2-15 port 1 temperature 1 1000V Al with Mitsui encap (notice file name has incorrect port assignment)
        filenamelocation = rootdir+'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined.csv'
        parameters = [1, 1, 0.05, 0.066, 0.001, 0.005, 0.1, 1, -1000, 'SubmergedMitsui', 150, 400, 'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined', 'placeholder', 1]
    elif n==23:    
        # 23 Damp Heat Al coupon 60/85 from 2/2/15 (notice file name has incorrect port assignment)
        filenamelocation = rootdir+'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined.csv'
        parameters = [2, 2, 0.005, 0.066, 0.001, 0.005, 0.1, 1, -1000, 'DH_60_85', 260, 520, 'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined', 'placeholder', 1]
    elif n==24:    
        # 24 Damp Heat Al coupon 60/85 from 2/2/15 edited to exclude bad readings
        filenamelocation = rootdir+'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined_edited.csv'
        parameters = [2, 2, 0.0033, 0.003, 0.0049, 0.005, 0.1, 1, -1000, 'DH_60_85', 10, 600, 'Data_port1temp2_DH_60C_85%_Al_w_defect_port2temp1_submerged_Al_mitsui_2_2_15_combined_edited', 'placeholder', 1]

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
    
#    Area1 = 0.15 # Portion of the length of L1 that has deep pitting
#    Area2 = 0.4 # Portion of length L1 that has medium pitting
#    Area3 = 0.45 # Portion of area with mild corrosion
#    Portion1 = 0.5 # percent of aluminum removal in area 1
#    Portion2 = 0.25 # percent of aluminum rmoval in area 2
#    Portion3 = 0.25 # percent of aluminum rmoval in area 3
#    
        # Set constants
    alphaAl = 4.29e-3 #Change of resistance with temperature in degC^-1
    rhoAl = 2.65E-08 #ohm-m at 20 degC
    MWAl = 26.98 #g/mol
    densityAl = 2.7 #g/cc
    NA = 6.022e23 #per mole
    ElecCoulomb = 6.24150965e18 # electrons per coulomb
    SecMinute = 60 #seconds per minute
    SecHour = 3600 #seconds per hour
    
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
       lvlist[i,36] = lvlist[i,MeasResColumn]*parameters[4]/((1+alpha*(lvlist[i,Thermocouple]-20))*parameters[2])       

    lvlist[0,21] = 1
       
    Rsum = 0
    Rsum2 = 0
    Rsumlength = 0
    timethreshold = 360
    Restime = 0
    AverageRes = numpy.zeros((5*parameters[11],numbercolumns))
    counter1 = 0
    
#   group and average resistance measurements
    for i in range(0,len(lvlist)-1):
        Rsum = Rsum + lvlist[i,MeasResColumn]
        Rsum2 = Rsum2 + lvlist[i,36] #to average R*w/L/temp adjust
        Rsumlength = Rsumlength + 1
        Restime = Restime + lvlist[i,20]
        if lvlist[i,21] > timethreshold: #for large gaps in time, report the average of the last batch of resistances
            AverageRes[counter1,1] = Rsum / Rsumlength
            AverageRes[counter1,0] = Restime / Rsumlength
            AverageRes[counter1,5] = Rsum2 / Rsumlength
            AverageRes[counter1,8] = lvlist[i,Thermocouple]
            AverageRes[counter1,9] = AverageRes[counter1,1]/(1+alpha*(AverageRes[counter1,8]-20))
            Rsum = 0
            Rsum2 = 0
            Rsumlength = 0
            Restime = 0
            counter1 = counter1 + 1
            
    for i in range(1,len(AverageRes[:,0])-1):
        AverageRes[i,2] = (AverageRes[i,0] - AverageRes[0,0])/3600
        AverageRes[i,3] = ((AverageRes[i,1] - AverageRes[i-1,1])/(AverageRes[i,2] - AverageRes[i-1,2]))*1000
        AverageRes[i,6] = ((AverageRes[i,5] - AverageRes[i-1,5])/(AverageRes[i,2] - AverageRes[i-1,2]))*1000   

    
    AverageRes[parameters[14],10] = 0.000037 #um of initial foil thickness
    
    for i in range(parameters[14]+1,len(AverageRes[:,0])-1):
        AverageRes[i,10] = 1/(((AverageRes[i,1]-AverageRes[i-1,1])*parameters[4]/rhoAl/parameters[2])+1/AverageRes[i-1,10])
        AverageRes[i,11] = (AverageRes[i,10]-AverageRes[i-1,10])/(AverageRes[i,2]-AverageRes[i-1,2])*1000000

    AverageResLen = 0
  
    for i in range(1,len(AverageRes[:,0])-1):
        if AverageRes[i,2] > 0:
            AverageResLen = AverageResLen + 1
       
             
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
#       hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
#       
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
#       hvlist[i,32] = (rhoAl * (L1*Area1/hvlist[i,29]/d+L1*Area2/hvlist[i,30]/d+L1*Area3/hvlist[i,31]/d+L2/h0/d) *(1+alphaAl*(hvlist[i,Temperaturecolumn]-20)))*1000 #calculated resistance in m-ohms 
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
    
             
    x=numpy.zeros(AverageResLen) #initiate vector to store times for regression
    y=numpy.zeros(AverageResLen) # initiate vector to store average resistances for regression
    y2 = numpy.zeros(AverageResLen)# for regression of R*w/L/temp adjust
    
    
    for i in range(AverageResLen):
    #    if AverageRes[i,2] >= parameters[10] and AverageRes[i,2] <= parameters[11]:
            x[i] = AverageRes[i,2]
            y[i] = AverageRes[i,1]
            y2[i] = AverageRes[i,5]
   
    #inds1 = indices(x, lambda x: x > parameters[10])
    #inds2 = indices(x, lambda x: x > parameters[11])
    #a1 = bisect.bisect(x, parameters[10])    
    #a2 = bisect.bisect(x, parameters[11])       
    
    regression = numpy.polyfit(x[parameters[10]:parameters[11]], y[parameters[10]:parameters[11]]*1000, 1)
    regression2 = numpy.polyfit(x[parameters[10]:parameters[11]], y2[parameters[10]:parameters[11]]*1000, 1)
    

    output = regression[0]/parameters[2]/parameters[4]
    print n
    print output     
    output = 0 
    
    for i in range(AverageResLen):
        AverageRes[i,4] = AverageRes[i,2]*regression[0]+regression[1]
        AverageRes[i,7] = AverageRes[i,2]*regression2[0]+regression2[1]

    
    #    Add up current over time to get total joules per time point
#        Then sum up the column (34) to get cummulative joules and divide by hoursover which the current was summed
    hvlinestart = 0
    hvlinestop = 0
    hvlinestart = [s for s, i in enumerate(hvlistcropped[:,33]) if i>AverageRes[parameters[10],2]][0]
    hvlinestop  = [s for s, i in enumerate(hvlistcropped[:,33]) if i>AverageRes[parameters[11]-1,2]][0]

    for i in range(hvlinestart,hvlinestop):
       hvlist[i,34] = (hvlist[i,33]-hvlist[i-1,33])*3600*hvlist[i,currentcolumn]
       hvlist[i,35] = hvlist[i,currentcolumn]
#       column 34 represents the number of seconds in the past time point times the current, which is equal to joules
    totaljoules = []
    totaljoules = numpy.sum(hvlist[:,34])
    Current_slope_output[n,0] = parameters[10]
    Current_slope_output[n,1] = parameters[11]
#    totaljoulesall[n,2] = totaljoules/(parameters[11]-parameters[10])
#    totaljoulesall[n,3] = sum(hvlist[:,34])/(hvlinestop-hvlinestart)
    Current_slope_output[n,4] = (sum(hvlist[hvlinestart:hvlinestop,currentcolumn]))/(hvlinestop-hvlinestart)
    Current_slope_output[n,5] = regression[0]
    Current_slope_output[n,6] = regression2[0]    
    Current_slope_output[n,7] = sum(AverageRes[parameters[14]:AverageResLen,11])/(AverageResLen-parameters[14])
    
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
    plt.plot(hvlist[0:-1,33],hvlist[0:-1,34]*(-100), 'g', linewidth=3.0)
    #plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
    ylabel('Resistance (m-ohms)',**font)
    plt.ylim([10,25])
    #plt.xlim([0,10])
    xlabel('Time (hrs)',**font)
    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance', **title_font)
    plt.legend(['Measured', 'Linear '+'y='+'%.5f' % regression[0]+'x+'+'%.5f' % regression[1]], loc='upper left')
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
    savefig(rootdir+'Resistance\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Resistance.png')
#    plt.show()
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
    #plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
    plt.plot(lvlist[:,33],lvlist[:,36]*1000,'ro')
    plt.plot(AverageRes[parameters[10]:parameters[11],2],AverageRes[parameters[10]:parameters[11],9]*1000, 'g', linewidth=3.0)
    plt.plot(AverageRes[parameters[14]:AverageResLen-1,2],AverageRes[parameters[14]:AverageResLen-1,10]*1000000, 'ko', linewidth=3.0)
#    plt.plot(hvlist[0:-1,33],hvlist[0:-1,34]*(-20), 'g', linewidth=3.0)
    #plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
    ylabel('Adjusted (temp) Resistance (m-ohms) and Remaining Al Thickness (um)',**font)
    plt.ylim([0,60])
    #plt.xlim([0,10])
    xlabel('Time (hrs)',**font)
    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance_Adjusted_temperature', **title_font)
    plt.legend(['Measured Res','Temp Adjusted Res', 'Remaining Thickness (um)'], loc='upper left')
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
    savefig(rootdir+'Adjusted Resistance\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Resistance_adjusted_temp_area.png')
   
    
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')   
    plt.plot(hvlist[0:-1,33],hvlist[0:-1,Temperaturecolumn],'b')
#    plt.plot(hvlist[0:-1,33],abs(hvlist[0:-1,MeasCurColumn]),'k')
    ylabel('Temperature (C))',**font)
#    plt.yscale('log')
    #plt.ylim([0,5])
#    plt.xlim([0,5])
    xlabel('Time (hrs)',**font)
#    title(r'Change in Calculated Resistance',**font)
    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Temperature', **title_font)
    #plt.legend(['Calculated', 'Measured'], loc='upper left')
    titlecurrent = filenamelocation.split
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'Temperature.png')
    savefig(rootdir+'Temperature\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Temperature.png')
    #    plt.show()
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
    
    plt.plot(AverageRes[0:AverageResLen,2],AverageRes[0:AverageResLen,3],'g')
    ylabel('Resistance Change (m-ohms/hr)',**font)
    #plt.ylim([0,5])
    #plt.xlim([0,10])
    xlabel('Time (hrs)',**font)
    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Change in Resistance', **title_font)
    #plt.legend(['Calculated', 'Measured'], loc='upper left')
    savefig(rootdir+'Resistance Change\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Resistance_Change.png')
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'ResistanceChange.png')
#    plt.show()
    
    figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')   
    plt.plot(hvlist[0:-1,33],hvlist[0:-1,MeasCurColumn]*1e9,'k')
    ylabel('Current (nA))',**font)
    plt.ylim([-500,0])
    #plt.xlim([0,10])
    xlabel('Time (hrs)',**font)
#    title(r'Change in Calculated Resistance',**font)
    title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Current', **title_font)
    #plt.legend(['Calculated', 'Measured'], loc='upper left')
    titlecurrent = filenamelocation.split
    savefig(rootdir+'Current\\'+'#'+str(n)+'_'+str(parameters[8])+'V_'+parameters[9]+'Port_'+str(parameters[0])+str(parameters[12])+'Current.png')
#        savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'Current.png')
#    plt.show()
    
    DataFile.close()