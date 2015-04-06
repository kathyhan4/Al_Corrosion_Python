# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 09:45:43 2015

@author: khan
"""

# A numerical application of Kat's corrosion model to predict remaining aluminum thickness

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

InitialThickness = 0.000037 # foil thickness in m

TimeStep = 60 # minutes
SimulationLength = 25 # years
TimePoints = SimulationLength * 365 * 24 * 60 / TimeStep

# Model Information from JMP
InterceptParam = 0.44888
VoltageParam = 0
TemperatureParam = 0
HumidityParam = 0
AverageCurrentParam = 2665807
VoltageTemperratureParam = 0
TemperatureHumidityParam = 0#-0.000331
InverseTempParam = -6492

ModelArray=numpy.zeros((TimePoints,20))

ModelArray[0,7] = InitialThickness # in m
ModelArray[0,0] = 0 # timepoint
ModelArray[0,1] = -100 # Voltage
ModelArray[0,2] = -.0000000002 # Current
ModelArray[0,3] = 40 # % relative humidity
ModelArray[0,4] = 40 # Temperature, deg C



for n in range(1,len(ModelArray)):
    ModelArray[n,0] = n # timepoint
    ModelArray[n,1] = -100 # Voltage
    ModelArray[n,2] = -.00000002 # Current - need to change this to A/m^2 eventually
    ModelArray[n,3] = 40 # % relative humidity
    ModelArray[n,4] = 40 # Temperature, deg C
    ModelArray[n,5] = (InterceptParam + ModelArray[n,1] * VoltageParam + ModelArray[n,2] * AverageCurrentParam + \
    ModelArray[n,3] * HumidityParam + ModelArray[n,4] * TemperatureParam +\
    (ModelArray[n,3]+740)*(ModelArray[n,4]-101) * VoltageTemperratureParam +\
    (ModelArray[n,4]-100)*(ModelArray[n,3]-85) * TemperatureHumidityParam +\
    InverseTempParam / (ModelArray[n,4]+273.15)) / 1000000# Al thickness change in m/hr
    ModelArray[n,6] = ModelArray[n,0] * TimeStep / 60 /24/365 # in years
    ModelArray[n,7] = ModelArray[n-1,7] + ModelArray[n,5] / 60 * TimeStep #final thickness of Al
    
font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 22}
title_font = {'fontname':'Arial', 'size':'12', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
matplotlib.rc('font', **font)
    
figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
#plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
plt.plot(ModelArray[:,6],ModelArray[:,7]*1000000,'ro')

#plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
ylabel('Al Thickness (um)',**font)
plt.ylim([0,40])
plt.xlim([0,25])
#plt.xlim([0,10])
xlabel('Time (years)',**font)
#title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance', **title_font)
#plt.legend(['Measured', 'Linear '+'y='+'%.5f' % regression[0]+'x+'+'%.5f' % regression[1]], loc='upper left')
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
savefig('C:\\Users\\khan\\Documents\\Al Corrosion\\Python Model Output\\'+'model.png')
#    plt.show()