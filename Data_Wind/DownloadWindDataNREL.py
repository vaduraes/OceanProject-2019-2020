#Download wind data from NREL
import h5pyd
import numpy as np
import xarray as xr
import time

#Hourly Wind Data from NREL
#Information available

#winddirection_100m
#winddirection_10m
#winddirection_120m
#winddirection_140m
#winddirection_160m
#winddirection_200m
#winddirection_40m
#winddirection_60m
#winddirection_80m
#windspeed_100m
#windspeed_10m
#windspeed_120m
#windspeed_140m
#windspeed_160m
#windspeed_200m
#windspeed_40m
#windspeed_60m
#windspeed_80m

#Inputs
LatNC=[34, 37] #Lower and upper bounds for Latitude  (NC region of interest)
LonNC=[-81,-74]#Lower and upper bounds for Longitude (NC region of interest)
Data_Name='windspeed_100m' #Name of file you want to get


Depth_NETCDF = xr.open_dataset("./Depths.nc")#File with bathymetry data
NREL = h5pyd.File("/nrel/wtk-us.h5", 'r') #Open conection with NREL server
        
#The original projection on NREL data is a modified Lambert Conic
Coordinates=NREL["coordinates"][:,:]#Coordinates in latitude longitude for each point y,x of the original data
 
XY_NC=[]#coordinates we are interested in downloading


#Get estimated depth in a given lat long
def GetDepth(Lat,Long):
    
    I_lat=np.argmin(np.square(Depth_NETCDF.lat.data-Lat))
    I_lon=np.argmin(np.square(Depth_NETCDF.lon.data-Long))
    
    depth=Depth_NETCDF.elevation.data[I_lat,I_lon]  
    
    return depth
    

#Get coordinates we are interested in downloading. 
#We group these coordinates such that we can decrease the total size of the file downloaded
for y in range(Coordinates.shape[0]):
    x_min=99999
    x_max=-1
    
    for x in range(Coordinates.shape[1]):
    
        if Coordinates[y,x]['lat']>=LatNC[0] and Coordinates[y,x]['lat']<=LatNC[1]\
        and Coordinates[y,x]['lon']>=LonNC[0] and Coordinates[y,x]['lon']<=LonNC[1]\
        and GetDepth(Coordinates[y,x]['lat'],Coordinates[y,x]['lon'])<0\
        and GetDepth(Coordinates[y,x]['lat'],Coordinates[y,x]['lon'])>-200:
            if x_min>x:
                x_min=x
            
            if x_max<x:
                x_max=x
            
    if x_max!=-1:
        XY_NC.append([y,x_min,x_max])

#Convert list to numpy array. This will facilitate future manipulation of this information
XY_NC = np.asarray(XY_NC, dtype=np.int)


#Downloading the data
i=-1
while i!=(len(XY_NC)-1):
    error=0
    i=i+1
    try:
        if i==0:
            #Create initial windspeed matrix and concatenate future wind data (windspeedTemp) on this same matrix
            windspeed=NREL[Data_Name][:,XY_NC[i,0],XY_NC[i,1]:XY_NC[i,2]+1]
        
        else:
            windspeedTemp=NREL[Data_Name][:,XY_NC[i,0],XY_NC[i,1]:XY_NC[i,2]+1]
            
        
        Lat=Coordinates['lat'][XY_NC[i,0],XY_NC[i,1]:XY_NC[i,2]+1]
        Lat=np.reshape(Lat,(len(Lat),1))
        
        Long=Coordinates['lon'][XY_NC[i,0],XY_NC[i,1]:XY_NC[i,2]+1]
        Long=np.reshape(Long,(len(Long),1))
    
    except:
        error=1
        i=i-1
        print("Error in the NREL server, too many requests- Waiting access release")
        time.sleep(61*60)
        NREL = h5pyd.File("/nrel/wtk-us.h5", 'r') #Open conection with NREL server
     
       
    if error==0:      
        if i==0:
            LatLong=np.concatenate((Lat,Long),axis=1)      
        else:
            LatLong=np.concatenate((LatLong,np.concatenate((Lat,Long),axis=1)),axis=0)
            windspeed=np.concatenate((windspeed,windspeedTemp),axis=1)

    print('Download----- %.1f%%'% ((i+1)/len(XY_NC)*100))
    
    
ReadMe='\
windspeed: m³\s \n\
LatLong: Latitude,Logitude data\n\
1) The data is in hourly discretization starting at 1/1/2007 and going up to\
12/31/2013 23:00'

np.savez('./'+ Data_Name +'.npz',ReadMe=ReadMe, windspeed=windspeed, LatLong=LatLong)

