#Geo plot of CF for wind energy
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

IndexOfInterest=5#Related to the feasible results of the optimization (CfFeasible)

OptimalPortfolioFile=np.load('PortlofioOPT1.npz',allow_pickle=True)

CfFeasible=OptimalPortfolioFile["CfFeasible"]


MILPSolutionsLatLongWind=OptimalPortfolioFile["MILPSolutionsLatLongWind"]
if MILPSolutionsLatLongWind.shape[0]!=0:
    MILPSolutionsLatLongWind=MILPSolutionsLatLongWind[IndexOfInterest]
    CF_EachOptimalSiteLocationWind=OptimalPortfolioFile["CF_EachOptimalSiteLocationWind"][IndexOfInterest]


MILPSolutionsLatLongWave=OptimalPortfolioFile["MILPSolutionsLatLongWave"]
if MILPSolutionsLatLongWave.shape[0]!=0:  
    MILPSolutionsLatLongWave=MILPSolutionsLatLongWave[IndexOfInterest]
    CF_EachOptimalSiteLocationWave=OptimalPortfolioFile["CF_EachOptimalSiteLocationWave"][IndexOfInterest]
    

MILPSolutionsLatLongOcean=OptimalPortfolioFile["MILPSolutionsLatLongOcean"]  
if MILPSolutionsLatLongOcean.shape[0]!=0:    
    MILPSolutionsLatLongOcean=MILPSolutionsLatLongOcean[IndexOfInterest]
    CF_EachOptimalSiteLocationOcean=OptimalPortfolioFile["CF_EachOptimalSiteLocationOcean"][IndexOfInterest]


ShapeFileCoast="./GEOData/ne_10m_coastline.shp"
ShapeFileStates="./GEOData/ne_10m_admin_1_states_provinces_lines.shp"

#All energy data
WindDataFile=np.load('WindEnergyNREL_100m_ERGIS.npz')
WindEnergyData=WindDataFile["WindEnergy"]
WindLatLongData=WindDataFile["LatLong"]

WaveDataFile=np.load('WaveEnergyRM3.npz')
WaveEnergyData=WaveDataFile["EnergyPu"]
WaveLatLongData=WaveDataFile["LatLong"]

OceanDataFile=np.load('CurrentEnergyRM4.npz')
OceanEnergyData=OceanDataFile["Energy_pu"]
OceanLatLongData=OceanDataFile["LatLong"]

AvgWindEnergy=np.average(WindEnergyData,axis=1)
AvgWaveEnergy=np.average(WaveEnergyData,axis=1)
AvgOceanEnergy=np.average(OceanEnergyData,axis=1)


#Wind geo plot
if MILPSolutionsLatLongWind.shape[0]!=0:  
    min_longitude=-78.7
    max_longitude=-74.6
    
    min_latitude=33.7
    max_latitude=36.7
    
    xlim =[min_longitude,max_longitude]
    ylim=[min_latitude, max_latitude]
    
    df = gpd.read_file(ShapeFileCoast)
    df1 = gpd.read_file(ShapeFileStates)
    
    fig, ax = plt.subplots(figsize  = None)
    
    df.plot(color='black',linewidth=1,ax=ax)
    df1.plot(color='black',linewidth=1,ax=ax)
    
    plt.scatter(WindLatLongData[:,1],WindLatLongData[:,0],c=AvgWindEnergy, s=0.2, cmap='jet')#Wind
    
    clb = plt.colorbar()
    clb.ax.set_title('CF')
    
    plt.scatter(MILPSolutionsLatLongWind[:,1], MILPSolutionsLatLongWind[:,0],s=20, facecolors='none', edgecolors='k',linewidth=0.5)#Wind
    plt.scatter(MILPSolutionsLatLongWind[:,1], MILPSolutionsLatLongWind[:,0],s=20, marker='+',c='k',linewidth=0.3)#Wind
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    plt.title("Optimal Wind Energy Portfolio, CF0="+str(CfFeasible[IndexOfInterest]))
    
    plt.savefig('OptimalPortfolioWind.png',dpi=700)
    plt.close()
    
    
#Wave geo plot
if MILPSolutionsLatLongWave.shape[0]!=0: 
    min_longitude=-78.7
    max_longitude=-74.5
    
    min_latitude=33.7
    max_latitude=36.7
    
    xlim =[min_longitude, max_longitude]
    ylim=[min_latitude, max_latitude]
    
    df = gpd.read_file(ShapeFileCoast)
    df1 = gpd.read_file(ShapeFileStates)
    
    fig, ax = plt.subplots(figsize  = None)
    
    df.plot(color='black',linewidth=1,ax=ax)
    df1.plot(color='black',linewidth=1,ax=ax)
    
    plt.scatter(WaveLatLongData[:,1], WaveLatLongData[:,0], c=AvgWaveEnergy, s=0.2, cmap='jet')
    
    clb = plt.colorbar()
    clb.ax.set_title('CF')
    
    plt.scatter(MILPSolutionsLatLongWave[:,1], MILPSolutionsLatLongWave[:,0],s=20, facecolors='none', edgecolors='k',linewidth=0.5)
    plt.scatter(MILPSolutionsLatLongWave[:,1], MILPSolutionsLatLongWave[:,0],s=20, marker='+',c='k',linewidth=0.3)
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    plt.title("Optimal Wave Energy Portfolio, CF0="+str(CfFeasible[IndexOfInterest]))
    
    plt.savefig('OptimalPortfolioWave.png', dpi=700)
    plt.close()

#Ocean current geo plot
if MILPSolutionsLatLongOcean.shape[0]!=0: 
    min_longitude=-77.1
    max_longitude=-74
    
    min_latitude=32.8
    max_latitude=36.1
    
    xlim =[min_longitude, max_longitude]
    ylim=[min_latitude, max_latitude]
    
    df = gpd.read_file(ShapeFileCoast)
    df1 = gpd.read_file(ShapeFileStates)
    
    fig, ax = plt.subplots(figsize  = None)
    
    df.plot(color='black',linewidth=1,ax=ax)
    df1.plot(color='black',linewidth=1,ax=ax)
    
    plt.scatter(OceanLatLongData[:,1], OceanLatLongData[:,0], c=AvgOceanEnergy, s=0.2, cmap='jet')
    
    clb = plt.colorbar()
    clb.ax.set_title('CF')
    
    plt.scatter(MILPSolutionsLatLongOcean[:,1], MILPSolutionsLatLongOcean[:,0],s=20, facecolors='none', edgecolors='k',linewidth=0.5)
    plt.scatter(MILPSolutionsLatLongOcean[:,1], MILPSolutionsLatLongOcean[:,0],s=20, marker='+',c='k',linewidth=0.3)
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    plt.title("Optimal Ocean  Portfolio CF0="+str(CfFeasible[IndexOfInterest]))
    
    plt.savefig('OptimalPortfolioOceanCurrent.png', dpi=700)
    plt.close()
 
    
#All Optimal site locations
min_longitude=-78.7
max_longitude=-74

min_latitude=32.8
max_latitude=36.7

xlim =[min_longitude, max_longitude]
ylim=[min_latitude, max_latitude]

df = gpd.read_file(ShapeFileCoast)
df1 = gpd.read_file(ShapeFileStates)

fig, ax = plt.subplots(figsize  = None)

df.plot(color='black',linewidth=1,ax=ax)
df1.plot(color='black',linewidth=1,ax=ax)

zs = np.concatenate([CF_EachOptimalSiteLocationWind, CF_EachOptimalSiteLocationWave, CF_EachOptimalSiteLocationOcean])
min_, max_ = zs.min(), zs.max()

if MILPSolutionsLatLongWind.shape[0]!=0:
    plt.scatter(MILPSolutionsLatLongWind[:,1], MILPSolutionsLatLongWind[:,0], c=CF_EachOptimalSiteLocationWind, cmap='jet',edgecolors='k',s=8, marker="^", label='Wind', linewidth=0.3)
    plt.clim(min_, max_)

if MILPSolutionsLatLongWave.shape[0]!=0: 
    plt.scatter(MILPSolutionsLatLongWave[:,1], MILPSolutionsLatLongWave[:,0], c=CF_EachOptimalSiteLocationWave, cmap='jet',edgecolors='k', s=8,  marker="s", label='Wave', linewidth=0.3)
    plt.clim(min_, max_)

if MILPSolutionsLatLongOcean.shape[0]!=0:
    plt.scatter(MILPSolutionsLatLongOcean[:,1], MILPSolutionsLatLongOcean[:,0], c=CF_EachOptimalSiteLocationOcean, cmap='jet',edgecolors='k',s=8, label='Current', linewidth=0.3)
    plt.clim(min_, max_)
    
plt.legend()
plt.colorbar().set_label('CF')


ax.set_xlim(xlim)
ax.set_ylim(ylim)
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.title("Optimal Portfolio CF0="+str(CfFeasible[IndexOfInterest]))

plt.savefig('OptimalPortfolioAllCases.png', dpi=700)
plt.close()  