1) To get the raw wave data and generate a .npz file with filtered data run:

PreprocessWaveData.py

Inputs: 
#TurbineFile> A file containing information of the wave turbine
#Depth_NETCDF> A file containing depth information for the ocean floor in the NC region
#NCWave> File with raw wave data, Hs and Tp(.mat)

Outputs:
#.npz file with filtered data for the wave resource 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2) To get wave energy run:

ComputeWaveEnergy.py

Inputs:
#TurbineFile: Wave turbine file. A txt file with the information needed for the wave turbine
#WaveData: Wave information for the turbine in hands (in Tp and Hs)

Outputs:
#.npz file with energy information (in pu units) for each feasible wave site location in the NC region. The information is in hourly discretization

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3) To generate a Geo plot for the capacity factor of wave resource run:

WaveCFGeoPlot.py

Inputs:
#ShapeFileCoast: Shapefile with information of the USA coast
#ShapeFileStates: Shapefile with information of the USA states
#HourlyData: Energy data for wave 

Outputs:
#.png geo plot showing the CF for the wave resource




#DATA NOT PROVIDED ON GITHUB:
#None