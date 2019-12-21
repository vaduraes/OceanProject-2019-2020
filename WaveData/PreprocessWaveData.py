#Preprocess wave raw data.
import numpy as np
import xarray as xr
from scipy.io import loadmat
from ReadTurbineData import ReadTurbineData

TurbineFile='WaveTurbineRM3_SAND.csv'
Turbine=ReadTurbineData(TurbineFile)
MinDepth=Turbine["MinDepth"]
MaxDepth=Turbine["MaxDepth"]

NCWave = loadmat('NCWaveparam.mat')
Depth_NETCDF = xr.open_dataset("./Depths.nc")

#Data time in the .mat file is in the julian format
StartTime=184080 #2000/01/01 to 2009/12/31 23:00. Determined by direct inspecting the .mat file

SitesMAT = NCWave['latlonNC']-1#latlonNC in the .mat is the index of sites in the NC region

#Compute depth in a given location
def GetDepth(Lat,Long):
    
    I_lat=np.argmin(np.square(Depth_NETCDF.lat.data-Lat))
    I_lon=np.argmin(np.square(Depth_NETCDF.lon.data-Long))
    
    distError=(np.square(Depth_NETCDF.lat.data[I_lat]-Lat)+np.square(Depth_NETCDF.lon.data[I_lon]-Long))**0.5
    
    depth=Depth_NETCDF.elevation.data[I_lat,I_lon]  
    
    return depth, distError

FeasibleSitesMAT=[]

IndexIn=[]# I have to keep track of two indexes because of the way the data was previously divided in the .mat file. 
#This index is for the wave information, the previous ("FeasibleSitesMAT") is for the lat long information

for i in range(len(SitesMAT)):
    Depth,Error=GetDepth(NCWave['latall'][SitesMAT[i]],NCWave['lonall'][SitesMAT[i]])#Get depth for each .mat site location
    
    #Upper and lower bounds for depth where the turbine can be installed
    if Depth<=-MinDepth and Depth>=-MaxDepth:
        FeasibleSitesMAT.append(SitesMAT[i])
        IndexIn.append(i)
    

FeasibleSitesMAT=np.array(FeasibleSitesMAT)
IndexIn=np.array(IndexIn)

NumSites=FeasibleSitesMAT.shape[0]

Longitude = np.reshape(NCWave['lonall'][FeasibleSitesMAT],(NumSites,1))

Latitude = np.reshape(NCWave['latall'][FeasibleSitesMAT],(NumSites,1))

LatLong=np.concatenate((Latitude,Longitude),axis=1)

HsNC = NCWave['HsNC'][IndexIn,StartTime:]
TpNC = NCWave['TpNC'][IndexIn,StartTime:]

ReadMe='\
HsNC: Significant wave height\n\
TpNC: Wave peak period\n\
1) The data is in hourly discretization starting at 1/1/2000 and going up to \
12/31/2009 23:00'

np.savez('WaveHsTp.npz', ReadMe=ReadMe, HsNC=HsNC, TpNC=TpNC, LatLong=LatLong)