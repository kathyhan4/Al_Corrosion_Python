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
import copy
__author__ = 'Ryan'

import numpy as np
from math import factorial

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError as msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')



rootdir= 'C:\\Users\\khan\\Documents\\GitHub\\AlCorrosionDataCSVFiles\\'
#filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon_aqueous_in_port_2_100_and_1000V_for_imaging_11_10_14.csv'
filenamelocation = rootdir+'Data_1A_500V_with_temp1_10_29_14_120hr.csv'
#filenamelocation = rootdir+'Data_1A_0V_with_temp1_10_27_14_120hr_control.csv'
#filenamelocation = rootdir+'Data_1A_100V_with_temp1_10_24_14_120hr.csv'
#filenamelocation = rootdir+'Data_1A_100V_with_temp1_10_31_14_120hr.csv'
#filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_15_14_24hr_new_Al.csv'
#filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_22_14_48hr.csv'
#filenamelocation = rootdir+'Data_1A_1000V_with_temp1_10_28_14_120hr.csv'
#filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_3_14_480hr_DH.csv'
#filenamelocation = rootdir+'Data_1A_1000V_with_temp2_11_7_14_480hr_DH_coupon.csv'
#filenamelocation = rootdir+'Data_100mA_100V_with_temp1_10_20_14_48hr.csv'
#filenamelocation = rootdir+'Data_Port1Temp2_DHAl_1000V_Port2Temp1_Cu_Aq_1000V_Port3Temp3Al_100Vimage.csv'
#filenamelocation = rootdir+'Data_DH_Port1_1000V_Temp2_maybe_more_P2_P3_11-26-14.csv'




DataFile = open(filenamelocation)
data = numpy.recfromcsv(DataFile, delimiter='\t', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')


size2=len(data[0])
numbercolumns = size2 + 15
Port = 1
Thermocouple = 2
currentcolumn = Port * 3 - 2 #second column for that port's data is current (Amps)
Temperaturecolumn = Thermocouple + 11
MeasResColumn = Port * 3 - 1
MeasCurColumn = Port * 3 - 2
MeasVoltColumn = Port * 3 - 3

#Set Inputs Specific to this Run
VoltageBias = -1000 #V
Current4Wire = 1 #1 amp in 4 wire measurement
OxidationState = 3 #electrons per Al atom in reaction
L1 = 0.05 #length of corroded area in m
L2 = 0.06 #length of non-corroded area in m
h0 = 0.000037 #thickness of foil initially in m
d = 0.005 #width of foil strip in m
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

Yn = numpy.zeros(len(lvlist[:,35]))

for i in len(lvlist[:,35]):
    Yn(i)=lvlist[i,35]

Smoothed = savitzky_golay(Yn, window_size=9, order=4)

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
plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
ylabel('Resistance (m-ohms)',**font)
plt.ylim([0,100])
#plt.xlim([0,10])
xlabel('Time (hrs)',**font)
title(r'Calculated Resistance',**font)
plt.legend(['Calculated', 'Measured'], loc='upper left')
savefig(filenamelocation.split('_resistance.')[0]+'.png')
plt.show()

figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')

plt.plot(lvlist[:,33],lvlist[:,35]*1000,'g')
ylabel('Resistance (m-ohms)',**font)
plt.ylim([0,100])
#plt.xlim([0,10])
xlabel('Time (hrs)',**font)
title(r'Change in Calculated Resistance',**font)
#plt.legend(['Calculated', 'Measured'], loc='upper left')
savefig(filenamelocation.split('_delRes.')[0]+'.png')
plt.show()

DataFile.close()