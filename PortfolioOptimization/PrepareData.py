#Prepare the data for the portfolio optimization
#Set time range and peculiarities of the simulation
#Remember to convert the pu values to a common pu base or the actual values

import numpy as np
import datetime as dt

def PrepareData():
    #The wind data starts at 1/1/2007 and ends at 12/31/2013
    WindE_File=np.load("../Data_Wind/WindEnergyNREL_100m_Haliade150_6MW.npz")# Wind energy File
    WindEnergy=WindE_File['WindEnergy']
    WindLatLong=WindE_File['LatLong']
    AnnualizedCostWind=WindE_File['AnnualizedCostWind']
    RatedPowerWind=float(WindE_File['RatedPower'])
    
    #The wave data starts at 1/1/2009 and ends at 12/31/2013
    WaveE_File=np.load('../Data_Wave/WaveEnergy_Pelamis_2009_2013.npz')# Wave energy File
    WaveEnergy=WaveE_File['Energy_pu']
    WaveLatLong=WaveE_File['LatLong']
    RatedPowerWave=float(WaveE_File['RatedPower'])
    AnnualizedCostWave=WaveE_File['AnnualizedCostWave']
    
    #The wave data starts at 1/1/2009 and ends at 11/30/2014
    OceanE_File=np.load('../Data_OceanCurrent/OceanCurrentEnergyRM4.npz')# Ocean current energy File
    OceanEnergy=OceanE_File['CurrentEnergy_pu']
    OceanLatLong=OceanE_File['LatLong']
    AnnualizedCostOcean=OceanE_File['AnnualizedCostOcean']
    RatedPowerOcean=float(OceanE_File['RatedPower'])
    
#-------------------------- WIND-----------------#
    SIdxWind=(dt.datetime(2009,1,1,0)-dt.datetime(2007,1,1,0)).days*24# Start index
    EIdxWind=(dt.datetime(2014,1,1,0)-dt.datetime(2007,1,1,0)).days*24# Last index
    
    Num3HourIntervals=int((EIdxWind-SIdxWind)/3)
    WindEnergy_Temp=np.zeros((WindEnergy.shape[0],Num3HourIntervals),dtype=float)
    
    for H3_Steps in range(Num3HourIntervals):
        
        StartIdx=SIdxWind + 3*(H3_Steps)
        
        WindEnergy_Temp[:,H3_Steps]=(WindEnergy[:,StartIdx])*RatedPowerWind
        
    WindEnergy=WindEnergy_Temp
    
    #Filter sites of wind energy with very low capacity factors
    AvgCFWind=np.average(WindEnergy,axis=1)/(RatedPowerWind)
    WindEnergy=WindEnergy[AvgCFWind>=0.20,:]
    WindLatLong=WindLatLong[AvgCFWind>=0.20,:]
    AnnualizedCostWind=AnnualizedCostWind[AvgCFWind>=0.20]
        
#-------------------------- WAVE-----------------#
    SIdxWave=(dt.datetime(2009,1,1,0)-dt.datetime(2009,1,1,0)).days*8
    EIdxWave=((dt.datetime(2014,1,1,0)-dt.datetime(2009,1,1,0)).days)*8
    WaveEnergy=WaveEnergy[:,SIdxWave:EIdxWave]*RatedPowerWave

    #Filter sites of wave energy with very low capacity factors
    AvgCFWave=np.average(WaveEnergy,axis=1)/(RatedPowerWave)
    
    WaveEnergy=WaveEnergy[AvgCFWave>=0.05,:]
    WaveLatLong=WaveLatLong[AvgCFWave>=0.05,:]
    AnnualizedCostWave=AnnualizedCostWave[AvgCFWave>=0.05]
    
#-------------------------- OCEAN CURRENT-----------------#   
    SIdxCurrent=(dt.datetime(2009,1,1,0)-dt.datetime(2009,1,1,0)).days*8
    EIdxCurrent=((dt.datetime(2014,1,1,0)-dt.datetime(2009,1,1,0)).days)*8
    OceanEnergy=OceanEnergy[:,SIdxCurrent:EIdxCurrent]*RatedPowerOcean
    
    #Filter oecan current for very low average capacity factors
    AvgCFOcean=np.average(OceanEnergy,axis=1)/(RatedPowerOcean)
    
    OceanEnergy=OceanEnergy[AvgCFOcean>=0.3,:]
    OceanLatLong=OceanLatLong[AvgCFOcean>=0.3,:]
    AnnualizedCostOcean=AnnualizedCostOcean[AvgCFOcean>=0.3]
  
	
    Data={"WindEnergy":WindEnergy,
          "WindLatLong":WindLatLong,
          "AnnualizedCostWind":AnnualizedCostWind,
          "WaveEnergy":WaveEnergy,
          "WaveLatLong":WaveLatLong,
          "AnnualizedCostWave":AnnualizedCostWave,
          "OceanEnergy":OceanEnergy,
          "OceanLatLong":OceanLatLong,
          "AnnualizedCostOcean":AnnualizedCostOcean,
          "RatedPowerWind":RatedPowerWind,
          "RatedPowerWave":RatedPowerWave,
          "RatedPowerOcean":RatedPowerOcean
          }
    
    return Data
