#Prepare the data for the portfolio optimization
#Set time range and peculiarities of the simulation
#Remember to convert the pu values to a common pu base or the actual values

#Summary
#--- Analysis for 2009
##-- Wind hourly
#--- Wave hourly
#--- Ocean current daily (interpolated to hourly)

import numpy as np
import datetime as dt

#IncludeWind=True
#IncludeWave=True
#IncludeCurrent=True

def PrepareData():
    WindE_File=np.load('WindEnergyNREL_100m_ERGIS.npz')# Wind energy File
    WindEnergy=WindE_File['WindEnergy']
    WindLatLong=WindE_File['LatLong']
    RatedPowerWind=float(WindE_File['RatedPower'])
    
    WaveE_File=np.load('WaveEnergyRM3.npz')# Wave energy File
    WaveEnergy=WaveE_File['EnergyPu']
    WaveLatLong=WaveE_File['LatLong']
    RatedPowerWave=float(WaveE_File['RatedPower'])
    
    OceanE_File=np.load('CurrentEnergyRM4.npz')# Ocean current energy File
    OceanEnergy=OceanE_File['Energy_pu']
    OceanLatLong=OceanE_File['LatLong']
    RatedPowerOcean=float(OceanE_File['RatedPower'])
    
    #Indexes for wind energy in the range of 1/1/2009 and 12/31/2009
    # (2007,1,1,0) is the start date for the wind resource
    SIdxWind=(dt.datetime(2009,1,1,0)-dt.datetime(2007,1,1,0)).days*24# Start index
    EIdxWind=(dt.datetime(2010,1,1,0)-dt.datetime(2007,1,1,0)).days*24# Last index
    
    WindEnergy=WindEnergy[:,SIdxWind:EIdxWind]*RatedPowerWind
    
    #Filter sites of wind energy with very low capacity factors
    AvgCFWind=np.average(WindEnergy,axis=1)
    
    WindEnergy=WindEnergy[AvgCFWind>=0.05*RatedPowerWind,:]
    WindLatLong=WindLatLong[AvgCFWind>=0.05*RatedPowerWind,:]
    
#    NumWindSites=WindEnergy.shape[0]
    
    #Indexes for wave energy in the range of 1/1/2009 and 12/31/2009
    # (2000,1,1,0) is the start date for the wave resource
    SIdxWave=(dt.datetime(2009,1,1,0)-dt.datetime(2000,1,1,0)).days*24
    EIdxWave=(dt.datetime(2010,1,1,0)-dt.datetime(2000,1,1,0)).days*24
    
    WaveEnergy=WaveEnergy[:,SIdxWave:EIdxWave]*RatedPowerWave
    
    #Filter sites of wave energy with very low capacity factors
    AvgCFWave=np.average(WaveEnergy,axis=1)
    
    WaveEnergy=WaveEnergy[AvgCFWave>=0.05*RatedPowerWave,:]
    WaveLatLong=WaveLatLong[AvgCFWave>=0.05*RatedPowerWave,:]
    
#    NumWaveSites=WaveEnergy.shape[0]
    
    #Indexes for ocean current energy in the range of 1/1/2009 and 12/31/2009
    # (2009,1,1,0) is the start date for the ocean current resource
    
    #-------------------Attention !!!!!
    #Currently, the informaiton that we have for ocean current is in daily discretization 
    #In order to simulate the model in hourly discretization we are going to repeate the daily data for
    #the 24 hours of the day
    SIdxCurrent=(dt.datetime(2009,1,1,0)-dt.datetime(2009,1,1,0)).days
    EIdxCurrent=(dt.datetime(2010,1,1,0)-dt.datetime(2009,1,1,0)).days
    
    OceanE_Daily=OceanEnergy[:,SIdxCurrent:EIdxCurrent]*RatedPowerOcean
    
    #Filter oecan current for very low average capacity factors
    AvgCFOcean=np.average(OceanE_Daily,axis=1)
    
    OceanE_Daily=OceanE_Daily[AvgCFOcean>=0.05*RatedPowerOcean,:]
    OceanLatLong=OceanLatLong[AvgCFOcean>=0.05*RatedPowerOcean,:]
    
    OceanEnergy=np.zeros((OceanE_Daily.shape[0],OceanE_Daily.shape[1]*24),dtype=float)
    
    #Repeate the daily data for the 24 hours of the day (Ocean current)
    for i in range(OceanE_Daily.shape[1]):
        OceanEnergy[:,i*24:(i+1)*24]=np.asarray([OceanE_Daily[:,i] for day in range(24)],dtype=float).T
             
#    NumOceanSites=OceanEnergy.shape[0]   
        
    Data={"WindEnergy":WindEnergy,
          "WindLatLong":WindLatLong,
          "WaveEnergy":WaveEnergy,
          "WaveLatLong":WaveLatLong,
          "OceanEnergy":OceanEnergy,
          "OceanLatLong":OceanLatLong,
          "RatedPowerWind":RatedPowerWind,
          "RatedPowerWave":RatedPowerWave,
          "RatedPowerOcean":RatedPowerOcean
          }
    return Data
