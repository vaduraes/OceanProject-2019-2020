#Get wind speed only for NREL offshore sites in the NC region
import numpy as np
import csv
import h5pyd
import xarray as xr


HubHeight=100

WindSpeedFile="windspeed_"+str(HubHeight)+"m.npz"

NREL_File="wtk_site_summary2007_2014_NC.csv" #File with the NC wind sites considered by the NREL


WindData=np.load(WindSpeedFile) 
RawWindspeed=WindData["windspeed"]
RawLatLong=WindData["LatLong"]


windspeed=[]
LatLong=[]
LatLong_NREL=[]


#Read NREL file and get lat long
with open(NREL_File) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count >=1:
            LatLong_NREL.append([row[2],row[1]])
            
        line_count += 1

LatLong_NREL=np.asarray(LatLong_NREL,dtype=float)


dist=[]#Smallest distance between the NREL site summary location and wind speed data
for i in range(LatLong_NREL.shape[0]):

    Dist=RawLatLong[:,:]-LatLong_NREL[i,:]
    Dist=np.linalg.norm(Dist,axis=1)
    
    Index=np.argmin(Dist)
    dist.append(Dist[Index])
    
    if Dist[Index]<=0.001:
        LatLong.append(RawLatLong[Index])
        windspeed.append(RawWindspeed[:,Index])
            
windspeed=np.asarray(windspeed,dtype=float)    
LatLong=np.asarray(LatLong,dtype=float)         


#####----
#Distance between two lat long points
def DistanceToShore (CoastLine, LatLong1): #Compute distance to shore in km of a lat long point
   
    CoastLine=CoastLine*2*np.pi/360
    LatLong1=LatLong1*2*np.pi/360
    
    LatLong1=np.reshape(LatLong1,(1,2))
    dLat=LatLong1[:,0]-CoastLine[:,0]
    dLong=LatLong1[:,1]-CoastLine[:,1]
    
    a=np.power(np.sin(dLat/2),2)+np.cos(CoastLine[:,0])*np.cos(LatLong1[:,0])*np.power(np.sin(dLong/2),2)
    c=2*np.arcsin(np.minimum(1,np.sqrt(a)))
    d=6367*c
    
    Distance=np.min(d) #Minimum distance to shore km
    
    return Distance


#Get coastline data
CoastLine=[]

File_CoastLine=open('./GEO_data/NC_Coastline.csv', "r")
File_CoastLine_csv=csv.reader(File_CoastLine,delimiter=',')

for EachLine in File_CoastLine_csv:

    if File_CoastLine_csv.line_num > 1:
        CoastLine.append([float(EachLine[1]), float(EachLine[0])] ) #LatLong

CoastLine=np.array(CoastLine)


Depth_NETCDF = xr.open_dataset("./Depths.nc")#File with bathymetry data

def GetDepth(Lat,Long):
    
    I_lat=np.argmin(np.square(Depth_NETCDF.lat.data-Lat))
    I_lon=np.argmin(np.square(Depth_NETCDF.lon.data-Long))
    
    depth=Depth_NETCDF.elevation.data[I_lat,I_lon]  
    
    return depth

Depth=[]
Distance2Shore=[]

for i in range(LatLong.shape[0]):
    Lat=LatLong[i,0]
    Long=LatLong[i,1]
    
    Depth.append(GetDepth(Lat,Long))
    Distance2Shore.append(DistanceToShore (CoastLine, np.array([Lat,Long])))
    
    
Depth=np.abs(np.array(Depth)) #[m]
Distance2Shore=np.array(Distance2Shore) #[km]
            
np.savez('./'+ "WindSpeedNREL_"+str(HubHeight)+"m" +'.npz',windspeed=windspeed,Depth=Depth,DistanceToShore=Distance2Shore,LatLong=LatLong)





