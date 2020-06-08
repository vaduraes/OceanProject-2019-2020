#Merge the data from HYCOM and MABSAB, keep the better resolution of MABSAB but allow the representation of
#hourly variability in the ocean current resource

import numpy as np
import csv
from ReadTurbineData import ReadTurbineData

TurbineFile='RM4Sandia.txt'

MABSAB_Dictionary=np.load("./MABSAB_DATA/CurrentSpeedMABSAB2009_2014.npz", allow_pickle=True)

LatLong_MABSAB = MABSAB_Dictionary["LatLong"]
CurrentSpeed_MABSAB = MABSAB_Dictionary["CurrentSpeed"]
RatedPower_MABSAB = MABSAB_Dictionary["RatedPower"]
DepthSites_MABSAB = MABSAB_Dictionary["DepthSites"]
ShoreDistance_MABSAB = MABSAB_Dictionary["ShoreDistance"]
OceanDateTime_MABSAB = MABSAB_Dictionary["OceanDateTime"]


HYCOM_Dictionary=np.load("./HYCOM_RAW_DATA/CurrentSpeedHYCOM2009_2014.npz", allow_pickle=True)
CurrentSpeedByDay_HYCOM=HYCOM_Dictionary['SpeedByDay_AllLatLong']
CurrentSpeed_HYCOM=HYCOM_Dictionary['Speed']
LatLong_HYCOM=HYCOM_Dictionary['LatLong']
DateTime_HYCOM=HYCOM_Dictionary["DateTime"]


#Get coastline data
CoastLine=[]

File_CoastLine=open('./GEO_data/Coastline_NC.csv', "r")
File_CoastLine_csv=csv.reader(File_CoastLine,delimiter=',')

for EachLine in File_CoastLine_csv:

    if File_CoastLine_csv.line_num > 1:
        CoastLine.append([float(EachLine[1]), float(EachLine[0])] ) #LatLong

CoastLine=np.array(CoastLine)

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

#For a deplyment of 200MVA
def EfficiencyTransmisison(LatLong):
    E_Transmission=[]
    for LatLong_i in LatLong:
        D=DistanceToShore(CoastLine, LatLong_i)
        if D<66:
            E_Transmission.append(-0.0362*D + 98.804)#HVAC
        else:
            E_Transmission.append(-0.0206*D + 96.432)#HVDC
            
    E_Transmission=np.array(E_Transmission)/100
    E_Transmission=np.reshape(E_Transmission,(len(E_Transmission),1))
    
    return E_Transmission

def DistanceBetweenLatLong(LatLong1, LatLong2):
    LatLong1=LatLong1*2*np.pi/360
    LatLong2=LatLong2*2*np.pi/360
    
    dLat=np.reshape(LatLong1[:,0],(len(LatLong1[:,0]),1))-np.reshape(LatLong2[:,0],(1,len(LatLong2[:,0])))
    dLong=np.reshape(LatLong1[:,1],(len(LatLong1[:,1]),1))-np.reshape(LatLong2[:,1],(1,len(LatLong2[:,1])))
    
    P1=np.repeat(np.reshape(np.cos(LatLong1[:,0]),(LatLong1.shape[0],1)),LatLong2.shape[0],axis=1)
    P2=np.repeat(np.reshape(np.cos(LatLong2[:,0]),(1,LatLong2.shape[0])),LatLong1.shape[0],axis=0)
    
    a=np.power(np.sin(dLat/2),2) + P1*P2*np.power(np.sin(dLong/2),2)
    c=2*np.arcsin(np.minimum(1,np.sqrt(a)))
    Distance=6367*c #[km]
    
    return Distance

#Convert ocean current speed to energy units
def Speed2Energy(Speed, Turbine, LatLong):
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
    Turbine['E_Collection']
    Turbine['Water_rho']
    Turbine['NumTurbinesPerSet']
    
    Area=np.pi*(Turbine['RotorDiamater']**2)/4
    
    Energy=(0.5*Turbine['C_Performance']*Turbine['Water_rho']*Turbine['Combined_E_Turbine']*Area*Speed**3)*Turbine['NumTurbinesPerSet']/Turbine['RatePower']
    Energy[Energy>1]=1
    
    Energy_pu=Energy*Turbine['Availability']*Turbine['E_Collection']
    
    E_Transmission=EfficiencyTransmisison(LatLong)
    Energy_pu=Energy_pu*E_Transmission
    
    return Energy_pu

#Making hycom and mabsab consistent in their time scale. They both start at 1/1/2009 but MABSAB end later than HYCOM
OceanDateTime_MABSAB=OceanDateTime_MABSAB[0:CurrentSpeedByDay_HYCOM.shape[1]]
CurrentSpeed_MABSAB=CurrentSpeed_MABSAB[:,0:CurrentSpeedByDay_HYCOM.shape[1]]

DailyAverage_Hycom=np.mean(CurrentSpeedByDay_HYCOM,axis=2,keepdims=True)

DailyAverage_Hycom=np.repeat(DailyAverage_Hycom,8,axis=2)
#Divide the daily values by the daily average, such that the average current speed in each day is always equal to one
CurrentSpeedByDay_HYCOM[DailyAverage_Hycom!=0]=CurrentSpeedByDay_HYCOM[DailyAverage_Hycom!=0]/DailyAverage_Hycom[DailyAverage_Hycom!=0]

Distance=DistanceBetweenLatLong(LatLong_MABSAB, LatLong_HYCOM)

#index of closest site location of hycom from a specific mabsab site location
IdxLatLong=np.argmin(Distance, axis=1)

HourlyData=np.zeros((CurrentSpeed_MABSAB.shape[0],CurrentSpeed_MABSAB.shape[1],8),dtype=float)

for i in range(len(LatLong_MABSAB)):
    HourlyData[i,:,:]=CurrentSpeedByDay_HYCOM[IdxLatLong[i],:,:]*np.repeat(np.reshape(CurrentSpeed_MABSAB[i,:],(CurrentSpeed_MABSAB.shape[1],1)),8,axis=1)

HourlyData=np.reshape(HourlyData,(HourlyData.shape[0],HourlyData.shape[1]*HourlyData.shape[2]))


Turbine=ReadTurbineData(TurbineFile)
CurrentEnergy=Speed2Energy(HourlyData, Turbine, LatLong_MABSAB)

ReadMe='\
CurrentEnergy_pu: Ocean current pu energy\m\
CurrentSpeed: Ocean current speed\n\
LatLong: Latitude,Logitude data\n\
DepthSites: Depth in each site location\n\
ShoreDistance: Smallest distance from site location to shore\n\
RatedPower: Rated power of the turbine model studied\n\
OceanDateTime: Time of the energy estimation\n'

np.savez("OceanCurrentEnergyRM4", ReadMe=ReadMe, CurrentEnergy_pu=CurrentEnergy, CurrentSpeed=HourlyData, LatLong=LatLong_MABSAB,
         DepthSites=DepthSites_MABSAB, ShoreDistance=ShoreDistance_MABSAB, RatedPower=RatedPower_MABSAB, OceanDateTime=DateTime_HYCOM)