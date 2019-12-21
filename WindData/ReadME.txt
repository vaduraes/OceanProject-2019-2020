1) To download NREL wind data (speed m3/s) run:

WindData_hsdsConfiguration.py
DownloadWindDataNREL.py

Inputs: 
#LatNC> Minimum and maximum values for Latitude 
#LonNC> Minimum and maximum values for Longitude
#Data_Name: Name of the file you want to download from the NREL database (available 10,40,60,80,100,120,140,160,200m. Wind speed and direction) 

Outputs:
#Wind speed and Lat Long for each wind speed measurements from 2007 to 2013 in hourly discretization

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2)To reduce the size of the wind speed data run:

GeneralWindSpeed_To_NRELSites.py

Inputs:
#HubHeight> Hub height for the turbine studied
#NREL_File> NREL file with the "feasible" site locations for wind turbines in the NC

Outputs:
#Wind speed and Lat Long for each wind speed measurements from 2007 to 2013 in hourly discretization just for the sites in the "NREL_File"

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3) To get wind energy run:

ComputeWindEnergy.py

Inputs:
#WindTurbine: Wind turbine file. A txt file with the information needed for the wind turbine
#"WindSpeedFile": Adequate winds speed file for the turbine in hands (in terms of hub height)

Outputs:
#.npz file with energy information (in pu units) for each feasible wind site location in the NC region. The information is in daily discretization

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

4) To generate a Geo plot for the capacity factor of wind resource run:

WindCFGeoPlot.py

Inputs:
#ShapeFileCoast: Shapefile with information of the USA coast
#ShapeFileStates: Shapefile with information of the USA states
#HourlyData: Energy data for wind 

Outputs:
#.png geo plot showing the CF for the wind resource




#DATA NOT PROVIDED ON GITHUB:
#windspeed_100m.npz> Raw data with wind speeds from NREL, >2GB. (We provided code so you can obtain this data by yourself)
#WindSpeedNREL_100m.npz> Data with wind speeds from NREL only in the feasible site locations, >0.8GB. (We provided code so you can obtain this data by yourself)
#WindEnergyNREL_100m_ERGIS.npz> Data with energy generated in each feasible location, >0.4GB. (We provided code so you can obtain this data by yourself)






