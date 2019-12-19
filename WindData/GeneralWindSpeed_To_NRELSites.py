#Get wind speed only for NREL offshore sites in the NC region
import numpy as np
import csv

HubHeight=100

WindSpeedFile="windspeed_"+str(HubHeight)+"m.npz"

NREL_File="wtk_site_summary2007_2014.csv" #File with the NC wind sites considered by the NREL


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
            
np.savez('./'+ "WindSpeedNREL_"+str(HubHeight)+"m" +'.npz',windspeed=windspeed,LatLong=LatLong)





