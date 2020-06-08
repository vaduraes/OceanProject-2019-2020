#Geo plot of CF for wave energy
import numpy as np
import geopandas as gpd
import datetime as dt
import csv
import matplotlib.colors as clrs
import matplotlib.pyplot as plt



ShapeFileCoast="./GEO_data/ne_10m_coastline.shp"
ShapeFileStates="./GEO_data/ne_10m_admin_1_states_provinces_lines.shp"

HourlyData=np.load('WaveEnergy_Pelamis_2009_2013.npz', allow_pickle=True)

HourlyEnergy=HourlyData["Energy_pu"]
AvgEnergy=np.average(HourlyEnergy,axis=1)
AnnualizedCostWave=HourlyData['AnnualizedCostWave']


LatLong=HourlyData["LatLong"]

LCOE=AnnualizedCostWave*10**6/(AvgEnergy*1.5*8766)

min_longitude=-78.7
max_longitude=-74.5

min_latitude=33.7
max_latitude=36.7

xlim =[min_longitude,max_longitude]
ylim=[min_latitude, max_latitude]

df = gpd.read_file(ShapeFileCoast)
df1 = gpd.read_file(ShapeFileStates)

fig, ax = plt.subplots(figsize  = None)

df.plot(color='black',linewidth=1,ax=ax)
df1.plot(color='black',linewidth=1,ax=ax)

plt.scatter(LatLong[:,1],LatLong[:,0], c=LCOE, s=0.2, cmap='jet')
#plt.clim(np.floor(min(LCOE)),500)

clb = plt.colorbar()
clb.ax.set_title('LCOE\n $/MWh')

ax.set_xlim(xlim)
ax.set_ylim(ylim)
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.title("Wave Energy LCOE\n(2009-2013)")

plt.savefig('LCOE_WaveNC_2009_2013.png',dpi=700)

