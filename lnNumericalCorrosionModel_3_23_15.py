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
import random


InitialThickness = 0.000037 # foil thickness in m

TimeStep = 60 # minutes
SimulationLength = 25 # years
TimePoints = SimulationLength * 365 * 24 * 60 / TimeStep

TimeNow = str(math.floor(time.time()))

AverageTemperature = 30 #deg C

# Model Information from JMP
InterceptParam = -4.909
InterceptParamLower95 = -6.25034
InterceptParamUpper95 = -3.56916
VoltageParam = 0
TemperatureParam = 0#0.0515
HumidityParam = 0
HumidityParamLower95 = 0
HumidityParamUpper95 = 0
AverageCurrentParam = 0
VoltageTemperratureParam = 0
TemperatureHumidityParam = 0
# Note that the inverse temperature parameter has a negative result on the rate of reaction compared to current and humidity
# so make sure to use the absolute lower of the 95% confidence interval numbers as the "upper 95%" and the 
# higher number (less negative or higher positive) as the lower 95% value
InverseTempParam = 0
InverseTempParamLower95 = 0
InverseTempParamUpper95 = 0
lnAbsAParam = 0.43965
lnAbsAParamLower95 = 0.12144
lnAbsAParamUpper95 = 0.75786
lnpH2OParam = 0

ModelArray=numpy.zeros((TimePoints,20))
ModelArrayLower95=numpy.zeros((TimePoints,20))
ModelArrayUpper95=numpy.zeros((TimePoints,20))

ModelArray[0,7] = InitialThickness * 1000000 # in um
ModelArray[0,0] = 0 # timepoint
ModelArray[0,1] = -1000 # Voltage
ModelArray[0,2] = 20 # Current
ModelArray[0,3] = 50 # % relative humidity
ModelArray[0,4] = 20 # Temperature, deg C

ModelArrayLower95[0,7] = InitialThickness * 1000000 # in um
ModelArrayLower95[0,0] = 0 # timepoint
ModelArrayLower95[0,1] = -1000 # Voltage
ModelArrayLower95[0,2] = 20 # Current
ModelArrayLower95[0,3] = 50 # % relative humidity
ModelArrayLower95[0,4] = 20 # Temperature, deg C

ModelArrayUpper95[0,7] = InitialThickness * 1000000 # in um
ModelArrayUpper95[0,0] = 0 # timepoint
ModelArrayUpper95[0,1] = -1000 # Voltage
ModelArrayUpper95[0,2] = 20 # Current
ModelArrayUpper95[0,3] = 50 # % relative humidity
ModelArrayUpper95[0,4] = 20 # Temperature, deg C

day = 0

for n in range(1,len(ModelArray)):
    ModelArray[n,0] = n # timepoint in hours
    ModelArray[n,1] = -1000 * math.sin(ModelArray[n,0]*math.pi/12) # Voltage
    if ModelArray[n,1] > 0:
        ModelArray[n,1] = 0
    ModelArray[n,2] = 20* math.sin(ModelArray[n,0]*math.pi/12-math.pi) # Current - need to change this to A/m^2 eventually
    if ModelArray[n,2] > 0:
        ModelArray[n,2] = -1e-15
    if ModelArray[n,2] == 0:
        ModelArray[n,2] = -1e-15
#    if ModelArray[n,2] < -1e-15:
#        ModelArray[n,2] = -1e-15
    ModelArray[n,3] = 50 # % relative humidity
    ModelArray[n,4] = AverageTemperature + 20 * math.sin(ModelArray[n,0]*math.pi/12) # Temperature, deg C
    
    ModelArray[n,5] = -exp((InterceptParam + ModelArray[n,1] * VoltageParam + ModelArray[n,2] * AverageCurrentParam + \
    ModelArray[n,3] * HumidityParam + ModelArray[n,4] * TemperatureParam +\
    InverseTempParam / (ModelArray[n,4]+273.15) + \
    (math.log(-1*ModelArray[n,2])) * lnAbsAParam)) # Al thickness change in m/hr
    
    ModelArray[n,6] = ModelArray[n,0] * TimeStep / 60 /24/365 # in years
    randomnumber = random.randrange(0, 1000, 1)
    if randomnumber < 50:
        ModelArray[n,7] = ModelArray[n-1,7] + ModelArray[n,5] / 60 * TimeStep #final thickness of Al
    else:
        ModelArray[n,7] = ModelArray[n-1,7]
    
for n in range(1,len(ModelArrayLower95)):
    ModelArrayLower95[n,0] = n # timepoint
    ModelArrayLower95[n,1] = -1000 * math.sin(ModelArrayLower95[n,0]*math.pi/12) # Voltage
    if ModelArrayLower95[n,1] > 0:
        ModelArrayLower95[n,1] = 0
    ModelArrayLower95[n,2] = 20* math.sin(ModelArrayLower95[n,0]*math.pi/12) # Current - need to change this to A/m^2 eventually
    if ModelArrayLower95[n,2] > 0:
        ModelArrayLower95[n,2] = -1e-15
    if ModelArrayLower95[n,2] == 0:
        ModelArrayLower95[n,2] = -1e-15
#    if ModelArray[n,2] < -1e-15:
#        ModelArray[n,2] = -1e-15
    ModelArrayLower95[n,3] = 50 # % relative humidity
    ModelArrayLower95[n,4] = AverageTemperature + 20 * math.sin(ModelArrayLower95[n,0]*math.pi/12) # Temperature, deg C
    
    ModelArrayLower95[n,5] = -exp((InterceptParamLower95 + ModelArrayLower95[n,1] * VoltageParam + ModelArrayLower95[n,2] * AverageCurrentParam + \
    ModelArrayLower95[n,3] * HumidityParamLower95 + ModelArrayLower95[n,4] * TemperatureParam +\
    InverseTempParamLower95 / (ModelArrayLower95[n,4]+273.15) + \
    (math.log(-1*ModelArrayLower95[n,2])) * lnAbsAParamLower95)) # Al thickness change in m/hr
    
    ModelArrayLower95[n,6] = ModelArrayLower95[n,0] * TimeStep / 60 /24/365 # in years
    randomnumber = random.randrange(0, 1000, 1)
    if randomnumber < 50:
        ModelArrayLower95[n,7] = ModelArrayLower95[n-1,7] + ModelArrayLower95[n,5] / 60 * TimeStep #final thickness of Al
    else:
        ModelArrayLower95[n,7] = ModelArrayLower95[n-1,7]
    
for n in range(1,len(ModelArrayUpper95)):
    ModelArrayUpper95[n,0] = n # timepoint
    ModelArrayUpper95[n,1] = -1000 * math.sin(ModelArrayUpper95[n,0]*math.pi/12) # Voltage
    if ModelArrayUpper95[n,1] > 0:
        ModelArrayUpper95[n,1] = 0
    ModelArrayUpper95[n,2] = 20* math.sin(ModelArrayUpper95[n,0]*math.pi/12) # Current - need to change this to A/m^2 eventually
    if ModelArrayUpper95[n,2] > 0:
        ModelArrayUpper95[n,2] = -1e-15
    if ModelArrayUpper95[n,2] == 0:
        ModelArrayUpper95[n,2] = -1e-15
#    if ModelArray[n,2] < -1e-15:
#        ModelArray[n,2] = -1e-15
    ModelArrayUpper95[n,3] = 50 # % relative humidity
    ModelArrayUpper95[n,4] = AverageTemperature + 20 * math.sin(ModelArrayUpper95[n,0]*math.pi/12) # Temperature, deg C
    
    ModelArrayUpper95[n,5] = -exp((InterceptParamUpper95 + ModelArrayUpper95[n,1] * VoltageParam + ModelArrayUpper95[n,2] * AverageCurrentParam + \
    ModelArrayUpper95[n,3] * HumidityParamUpper95 + ModelArrayUpper95[n,4] * TemperatureParam +\
    InverseTempParamUpper95 / (ModelArrayUpper95[n,4]+273.15) + \
    (math.log(-1*ModelArrayUpper95[n,2])) * lnAbsAParamUpper95)) # Al thickness change in m/hr
    
    ModelArrayUpper95[n,6] = ModelArrayUpper95[n,0] * TimeStep / 60 /24/365 # in years
    # Random number generator determines if it is raining during this time period.  
    randomnumber = random.randrange(0, 1000, 1)
    if randomnumber < 50:
        ModelArrayUpper95[n,7] = ModelArrayUpper95[n-1,7] + ModelArrayUpper95[n,5] / 60 * TimeStep #final thickness of Al
    else:
        ModelArrayUpper95[n,7] = ModelArrayUpper95[n-1,7]
     

font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 22}
title_font = {'fontname':'Arial', 'size':'12', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
matplotlib.rc('font', **font)
    
figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
#plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
plt.plot(ModelArray[:,6],ModelArray[:,7],'r')
plt.plot(ModelArrayLower95[:,6],ModelArrayLower95[:,7],'b')
plt.plot(ModelArrayUpper95[:,6],ModelArrayUpper95[:,7],'g')
#plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
ylabel('Al Thickness (um)',**font)
plt.ylim([0,40])
plt.xlim([0,25])
#plt.xlim([0,10])
xlabel('Time (years)',**font)
#title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance', **title_font)
#plt.legend(['Measured', 'Linear '+'y='+'%.5f' % regression[0]+'x+'+'%.5f' % regression[1]], loc='upper left')
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
savefig('C:\\Users\\khan\\Documents\\GitHub\\Python_model_output\\'+'model'+TimeNow+'.png')
#    plt.show()

figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
#plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
plt.plot(ModelArray[1:24,0],ModelArray[1:24,3],'r')
plt.plot(ModelArray[1:24,0],ModelArray[1:24,4],'b')
plt.legend(['Humidity (%)','Temperature (C)'], loc='upper left')
#plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
ylabel('Temperature and Humidity',**font)
plt.ylim([0,100])
plt.xlim([0,24])
#plt.xlim([0,10])
xlabel('Time (hours)',**font)
#title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance', **title_font)
#plt.legend(['Measured', 'Linear '+'y='+'%.5f' % regression[0]+'x+'+'%.5f' % regression[1]], loc='upper left')
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
savefig('C:\\Users\\khan\\Documents\\GitHub\\Python_model_output\\'+'one_day_T_RH'+TimeNow+'.png')
#    plt.show()
figure(num=None, figsize=(12, 8), dpi=480, facecolor='w', edgecolor='k')
#plt.plot(hvlistcropped[0:-2,33],hvlistcropped[0:-2,32])
plt.plot(ModelArray[1:24,0],ModelArray[1:24,2],'k')

#plt.plot(lvlist[:,33],lvlist[:,34]*1000,'g')
ylabel('Current',**font)
#plt.ylim([0,100])
plt.xlim([0,24])
#plt.xlim([0,10])
xlabel('Time (hours)',**font)
#title(str(n)+'_'+parameters[12]+parameters[9]+'Port_'+str(parameters[0])+'Resistance', **title_font)
#plt.legend(['Measured', 'Linear '+'y='+'%.5f' % regression[0]+'x+'+'%.5f' % regression[1]], loc='upper left')
#    savefig(filenamelocation.split('.csv')[0]+'_#'+str(n)+'_'+parameters[9]+'Port_'+str(parameters[0])+'.png')
savefig('C:\\Users\\khan\\Documents\\GitHub\\Python_model_output\\'+'one_day_current'+TimeNow+'.png')