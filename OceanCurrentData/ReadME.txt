1)To compute current energy in each site location run:

ComputeCurrentEnergy.py

Inputs:
#TurbineFile> .txt file with the turbine information (e.g. RM4Sandia.txt)
#CurrentRawData> Raw data with current speed (.mat)
#DepthDomain> depth domain for the speed data (.mat)

Outputs:
#.npz file with energy generated in each feasible site location

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2) To generate a Geo plot for the capacity factor of current resource run:
	
CurrentCFGeoPlot.py

Inputs:
#ShapeFileCoast: Shapefile with information of the USA coast
#ShapeFileStates: Shapefile with information of the USA states
#HourlyData: Energy data for current 

Outputs:
#.png geo plot showing the CF for the currrent resource


#DATA NOT PROVIDED ON GITHUB:
#2009.mat> Raw data with current speeds, >2GB. (We don`t have a path for sharing this data yet)





