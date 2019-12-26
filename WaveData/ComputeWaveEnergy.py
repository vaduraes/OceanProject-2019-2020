#Compute wave energy
import numpy as np
from ReadTurbineData import ReadTurbineData

#Get turbine data
TurbineFile='WaveTurbineRM3_SAND.csv'
Turbine=ReadTurbineData(TurbineFile)

RatedPower=Turbine["RatedPower"]
E_Mec2El=Turbine["E_Mec2El"]
E_Av=Turbine["E_Av"]
E_Tr=Turbine["E_Tr"]
Te_Bins=Turbine["Te_Bins"]
Hs_Bins=Turbine["Hs_Bins"]
MP_Matrix=Turbine["MP_Matrix"]

#Get wave data
WaveData='WaveHsTp.npz'
WaveFile=np.load(WaveData)
HsNC=WaveFile["HsNC"]
TpNC=WaveFile["TpNC"]

LatLong=WaveFile["LatLong"]

HsShape=HsNC.shape

#Create an one dimensional vector with the Hs data. This procedure facilitates significantly the future steps
D1_HsNC=np.reshape(HsNC,(np.size(HsNC),1))

#Index of the Hs set value closest to the observed Hs value
IdxHs=np.reshape(np.argmin(np.abs(D1_HsNC-Hs_Bins.T),axis=1), HsShape)

#Create an one dimensional vector with the To data.
D1_TpNC=np.reshape(TpNC,(np.size(TpNC),1))

#Index of the Tp set value closest to the observed Tp value
IdxTp=np.reshape(np.argmin(np.abs(D1_TpNC-Te_Bins.T),axis=1),HsShape)

EnergyProduction=np.minimum(MP_Matrix[IdxHs,IdxTp]*E_Mec2El,RatedPower)

EnergyPu=EnergyProduction/RatedPower

EnergyPu=EnergyPu*E_Av#Attention transmisson was not considered here

ReadMe='\
EnergyPu: pu wave energy (Base 300kw) 1 unit per site\n\
1) The data is in hourly discretization starting at 1/1/2000 and going up to\
 12/31/2009 23:00'

np.savez('WaveEnergyRM3.npz',ReadMe=ReadMe, EnergyPu=EnergyPu,RatedPower=RatedPower, LatLong=LatLong)