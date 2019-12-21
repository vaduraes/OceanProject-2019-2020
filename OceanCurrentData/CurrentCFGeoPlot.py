#Geo plot of CF for ocean current energy
import numpy as np
import pandas as pd
import geoplot as gplt
import geopandas as gpd
import matplotlib.colors as clrs
import matplotlib.pyplot as plt


ShapeFileCoast="./GEO_data/ne_10m_coastline.shp"
ShapeFileStates="./GEO_data/ne_10m_admin_1_states_provinces_lines.shp"

HourlyData=np.load('CurrentEnergyRM4.npz')

HourlyCurrentEnergy=HourlyData["Energy_pu"]
AvgCurrentEnergy=np.average(HourlyCurrentEnergy,axis=1)

LatLong=HourlyData["LatLong"]


min_longitude=-77
max_longitude=-74

min_latitude=33
max_latitude=36.2

xlim =[min_longitude,max_longitude]
ylim=[min_latitude, max_latitude]

df = gpd.read_file(ShapeFileCoast)
df1 = gpd.read_file(ShapeFileStates)

fig, ax = plt.subplots(figsize  = None)

df.plot(color='black',linewidth=1,ax=ax)
df1.plot(color='black',linewidth=1,ax=ax)

plt.scatter(LatLong[:,1],LatLong[:,0],c=AvgCurrentEnergy, s=0.2, cmap='jet')

clb = plt.colorbar()
clb.ax.set_title('CF')

ax.set_xlim(xlim)
ax.set_ylim(ylim)
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.title("Ocean Current Energy Sites")

plt.savefig('CF_CurrentNC_2009.png',dpi=700)

