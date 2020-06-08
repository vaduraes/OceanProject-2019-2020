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
#LCOE_Max> Array with the LCOEs you want to investigate
#Nt> Total number of installed turbine units [Wind,Wave,Ocean],(Can handle zero values).
#NuWiWaOcean> Upper bound for the number of installed turbines in a single cell [Wind,Wave,Ocean]






         




Outputs:
#A .npz file with the following information:

------Step 1
1) TotalNumTurbines: Total number of turbines (Wind,Wave,Ocean Current)
2) MaxNumTurbines: Maximum number of turbines per grid cell (Wind,Wave,Ocean Current)
3) FeasibilityStep1: Equals to 1 if the LCOE target could be attained 0 if it could not (step1)
4) RelaxedLCOETarget: LCOEs simulated by the relaxed portfolio optimization (all cases including infeasible ones)
5) RelaxedSolutionsLCOE: Values of LCOE for the portfolios in the relaxed MINLP (after optimization- step1)
6) RelaxedSolutionsVar: Values of variance for the portfolios in the relaxed MINLP (step1)
7) OptimalXSolutionsWind: Number of wind turbines in each optimal site location for the relaxed MINLP
8) OptimalXSolutionsWave: Number of wave turbines in each optimal site location for the relaxed MINLP
9) OptimalXSolutionsOcean: Number of ocean current turbines in each optimal site location for the relaxed MILP
10)OptimalSSolution: Optimal solution for the "s" variables
11)OptimalKSolution: Optimal solution for the "k" variables
12)RelaxedSolutionsLatLongWind: LatLong of each optimal wind site location for the relaxed MINLP
13)RelaxedSolutionsLatLongWave: LatLong of each optimal wave site location for the relaxed MINLP
14)RelaxedSolutionsLatLongOcean: LatLong of each optimal ocean current site location for the relaxed MINLP

------Step 2

15)FeasibilityStep2: Equals to 1 if the LCOE target could be attained 0 if it could not (step2)
16)MINLPSolutionsLCOE: Values of LCOE for the portfolios in the relaxed MINLP (after optimization- step2)
17)MINLPSolutionsVar: Values of variance for the portfolios in the relaxed MINLP (step2)
18)OptimalYSolutionsWind: Number of wind turbines in each optimal site location for the MINLP
19)MINLPSolutionsLatLongWind: LatLong of each optimal wind site location for the MINLP (step2)
20)OptimalYSolutionsWave: Number of wave turbines in each optimal site location for the MINLP
21)MINLPSolutionsLatLongWave: LatLong of each optimal wave site location for the MINLP
22)OptimalYSolutionsOcean: Number of ocean current turbines in each optimal site location for the MINLP
23)MINLPSolutionsLatLongOcean: LatLong of each optimal ocean current site location for the MINLP
24)elapsed_time: total clock time
25)E_CPU_TIME: total cpu time

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3)To generate a graph comparing LCOE X variance for the optimized portfolio run:

EfficientFrontier.py

Inputs:
#Portfolio> The results from the portfolio optimization

Output:
#.png file with the graph

