#Ocean current data 

import numpy as np
import datetime as dt
from scipy.io import loadmat
from ReadTurbineData import ReadTurbineData

#Convert ocean current speed to energy units
def Speed2Energy(Speed, Turbine):
#Power equation from- 2.3.1.1 Performance Analysis and AEP Estimation, of https://energy.sandia.gov/energy/renewable-energy/water-power/technology-development/reference-model-project-rmp/

    Turbine['RatePower']
    Turbine['RotorDiamater']
    Turbine['C_Performance']
    Turbine['E_Gearbox']
    Turbine['E_Generator']
    Turbine['E_Transformer']
    Turbine['E_Inverter']
    Turbine['Combined_E_Turbine']
    Turbine['Availability']
    Turbine['E_Transmission']
    Turbine['Water_rho']
    Turbine['NumTurbinesPerSet']
    
    Area=np.pi*(Turbine['RotorDiamater']**2)/4
    
    Energy=(0.5*Turbine['C_Performance']*Turbine['Water_rho']*Turbine['Combined_E_Turbine']*Area*Speed**3)*Turbine['NumTurbinesPerSet']/Turbine['RatePower']
    Energy[Energy>1]=1
    
    Energy_pu=Energy*Turbine['Availability']*Turbine['E_Transmission']
    
    return Energy_pu

TurbineFile='RM4Sandia.txt'
Turbine=ReadTurbineData(TurbineFile)
RotorDepth=Turbine["RotorDepth"]

MinDepth=Turbine["MinDepth"]
MaxDepth=Turbine["MaxDepth"]

RatedPower=Turbine["RatePower"]

DepthDomain= loadmat('depth_domain.mat')
SitDepth=DepthDomain["h"]
DepthLayers=DepthDomain["depth_rho0"]

#Get the feasible site locations based on the maximum and minimum depths
IndexFDepth=((SitDepth<=MaxDepth) & (SitDepth>=MinDepth))

#Get index closest to the rated depth of operation for the turbine (RotorDepth)
IndexTurbineDepth=(np.argmin(np.abs(DepthLayers-RotorDepth),axis=2))[IndexFDepth]

CurrentRawData= loadmat('2009.mat')

ocean_time=CurrentRawData['ocean_time']

lon_range=CurrentRawData['lon_range']
lat_range=CurrentRawData['lat_range']

#Ocean current speed filtered for feasible site locations
udata=CurrentRawData['udata'][IndexFDepth,:,:]#speed towards east (Zonal velocity)
vdata=CurrentRawData['vdata'][IndexFDepth,:,:]#speed towards north (Meridional velocity)

#Filter speed to get only the depth closest to the rated depth
u_filtered=np.zeros((udata.shape[0],udata.shape[2]),dtype=float)
v_filtered=np.zeros((udata.shape[0],udata.shape[2]),dtype=float)

for site in range(udata.shape[0]):
    u_filtered[site,:]=udata[site,IndexTurbineDepth[site],:]
    v_filtered[site,:]=vdata[site,IndexTurbineDepth[site],:]

#Get the magnitude of the speed vector
Speed=np.sqrt(u_filtered**2+v_filtered**2)

#Release RAM memory
del(CurrentRawData, udata, vdata, u_filtered, v_filtered)

DimLat=lat_range.shape[1]
DimLong=lon_range.shape[0]

#Organize the data 
lon_range=np.repeat(lon_range,DimLat,axis=1).T
lat_range=np.repeat(lat_range,DimLong,axis=0).T

LatLong=np.zeros((np.sum(IndexFDepth),2),dtype=float)

LatLong[:,0]=lat_range[IndexFDepth]
LatLong[:,1]=lon_range[IndexFDepth]


#Get Time 
OceanDateTime=[]
for i in range(ocean_time.shape[0]):
    OceanDateTime.append(dt.timedelta(seconds=ocean_time[i,0]) + dt.datetime(1858,11,17,0,0,0))


Energy_pu=Speed2Energy(Speed, Turbine)

ReadMe='\
Energy_pu: Energy in pu units\
LatLong: Latitude,Logitude data\n\
1) The data is in Daily discretization starting at 1/1/2009 and going up to \
1/2/2010'


np.savez('CurrentEnergyRM4.npz',ReadMe=ReadMe,Energy_pu=Energy_pu,RatedPower=RatedPower,LatLong=LatLong,OceanDateTime=OceanDateTime)