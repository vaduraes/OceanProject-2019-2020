#Compute wave energy

import numpy as np
from ReadTurbineData import ReadTurbineData

#Get turbine data
TurbineFile='Pelamis.csv'
Turbine=ReadTurbineData(TurbineFile)

RatedPower=Turbine["RatedPower"]
E_Mec2El=Turbine["E_Mec2El"]
E_Av=Turbine["E_Av"]
E_Tr=Turbine["E_Tr"]
Te_Bins=Turbine["Te_Bins"]
Hs_Bins=Turbine["Hs_Bins"]
MP_Matrix=Turbine["MP_Matrix"]

#Get wave data
WaveData='WaveHsTp_WWIII.npz'
WaveFile=np.load(WaveData)
HsNC=WaveFile["HsNC"]
TpNC=WaveFile["TpNC"]

LatLong=WaveFile["LatLong"]

HsShape=HsNC.shape

#Create an one dimensional vector with the Hs data. This procedure facilitates significantly the future steps
D1_HsNC=np.reshape(HsNC,(np.size(HsNC),1))

#Index of the Hs set value closest to the observed Hs value
IdxHs=np.reshape(np.argmin(np.abs(D1_HsNC-Hs_Bins.T),axis=1), HsShape)

#Create an one dimensional vector with the Tp data.
D1_TpNC=np.reshape(TpNC,(np.size(TpNC),1))

#Index of the Tp set value closest to the observed Tp value
IdxTp=np.reshape(np.argmin(np.abs(D1_TpNC-Te_Bins.T),axis=1),HsShape)

EnergyProduction=np.minimum(MP_Matrix[IdxHs,IdxTp]*E_Mec2El,RatedPower)

WakeEffect=0.95
EnergyPu=EnergyProduction/RatedPower*WakeEffect

EnergyPu=EnergyPu*E_Av*E_Tr

ReadMe='\
EnergyPu: pu wave energy (Base 1.5MVA) 1 unit per site\n\
1) The data is in hourly discretization starting at 1/1/2009 and going up to\
 31/12/2013'

np.savez('WaveEnergy_Pelamis_2009_2013.npz',ReadMe=ReadMe, EnergyPu=EnergyPu, RatedPower=RatedPower, LatLong=LatLong,\
         Depth=WaveFile["Depth"], ShoreDistance=WaveFile["ShoreDistance"])