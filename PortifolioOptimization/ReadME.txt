0) In order to do the portfolio optimization, you first need to prepare your data. 
This step is performed by PrepareData.py (function PrepareData)

This function can be modified as the user desire but has to generate as output energy and LatLong values for wind, wave, and ocean only
for the site locations you desire to incorporate in the optimization process.

Also, the data for wind, wave, and ocean current must have the same number of time intervals and must be at the same start and end time (date); and
remember to convert the pu values to the actual values

Inputs: 
#WindE_File> .npz file with wind energy information (Latitude, longitude and enegy generation in each site location)
#WaveE_File> .npz file with wave energy information
#OceanE_File> .npz file with ocean current energy information

Outputs:
#Dictionary with all data necessary for the optimization process

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2)To compute the optimized portfolio run:

PortfolioOptimization.py

Inputs:
#CF0> Array with the capacity factors you want to investigate
#Nt> Total number of installed turbine units [Wind,Wave,Ocean],(Can handle zero values).
#NuWiWaOcean> Upper bound for the number of installed turbines in a single cell [Wind,Wave,Ocean]
#Ns> Upper bound for the number of selected sities [Wind,Wave,Ocean]

Outputs:
#A .npz file with the following information:
1) CfFeasible: CF simulated by the LP problem (Feasible)
2) CfSimulated: CF simulated by the portfolio optimization (all cases including infeasible ones)
3) TotalNumTurbines: Total number of turbines (Wind,Wave,Ocean Current)
4) MaxNumTurbines: Maximum number of turbines per grid cell (Wind,Wave,Ocean Current)
5) MaxNumSites: Maximum number of site locations (Wind,Wave,Ocean Current)
6) RelaxedSolutionsCF: Values of CF for the portfolios in the relaxed MILP (after optimization)
7) RelaxedSolutionsVar: Values of variance for the portfolios in the relaxed MILP
8) OptimalXSolutionsWind: Number of wind turbines in each optimal site location for the relaxed MILP
9) OptimalXSolutionsWave: Number of wave turbines in each optimal site location for the relaxed MILP
10) OptimalXSolutionsOcean: Number of ocean current turbines in each optimal site location for the relaxed MILP
11) RelaxedSolutionsLatLongWind: LatLong of each optimal wind site location for the relaxed MILP
12) RelaxedSolutionsLatLongWave: LatLong of each optimal wave site location for the relaxed MILP
13) RelaxedSolutionsLatLongOcean: LatLong of each optimal ocean current site location for the relaxed MILP
14) MILPSolutionsCF: Values of CF for the portfolios in the  MILP (after optimization)
15) MILPSolutionsVar: Values of variance for the portfolios in the MILP
16) OptimalYSolutionsWind: Number of wind turbines in each optimal site location for the MILP
17) OptimalYSolutionsWave: Number of wave turbines in each optimal site location for the MILP
18) OptimalYSolutionsOcean: Number of ocean current turbines in each optimal site location for the MILP
19) MILPSolutionsLatlongWind: LatLong of each optimal wind site location for the MILP
20) MILPSolutionsLatlongWave: LatLong of each optimal wave site location for the MILP
21) MILPSolutionsLatlongOcean: LatLong of each optimal ocean current site location for the MILP
22) TotalSimulationTime= Total processing time [seconds]
23) CF_EachOptimalSiteLocationWind=  Average CF for each optimal wind site location
24) CF_EachOptimalSiteLocationWave=  Average CF for each optimal wave site location
25) CF_EachOptimalSiteLocationOcean= Average CF for each optimal ocean current site location

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3)To generate a graph comparing CF X variance for the optimized portfolio run:

CFxVariance.py

Inputs:
#OptimizationResults> The results from the portfolio optimization

Output:
#.png file with the graph

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3)To generate a geo plot for a specific solution of the portfolio optimization run:

GeoPlot.py

Inputs:
#OptimalPortfolioFile> The results from the portfolio optimization
#IndexOfInterest> Index from the feasible CF0 simulation that you whant the plot (Choose index based on CfFeasible)

Output:
#1) A geo plot for wind, wave, and ocean current separately showing the CF in all site locations and the location of the optimal sites.
#2) A geo plot with the optimal site locations for wind wave and ocean together. (Here we only show the optimal site locaitons)


