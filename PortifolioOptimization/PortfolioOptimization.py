#Portfolio optimization all three sources
from __future__ import division
from pyomo.environ import *
from PrepareData import PrepareData
import numpy as np
import time
start_time = time.time()

CF0=np.array([i for i in range(10,82,2)])/100# Target capacity factor (0.1 a 0.8 in steps o 0.02)

Nt=[10,0,10]# Total number of installed turbine units Wind/Wave/Ocean

#Upper bound for the number of installed turbines in a single cell Wind/Wave/Ocean
NuWiWaOcean=[8,4,4]

#Upper bound for the number of selected sities Wind/Wave/Ocean
Ns=[4,4,4]

Data=PrepareData()

WindEnergy=Data["WindEnergy"]
WindEnergy=WindEnergy[1:100,:]
WindLatLong=Data["WindLatLong"]
WindLatLong=WindLatLong[1:100,:]
NumWindSites=WindEnergy.shape[0]
RatedPowerWind=Data["RatedPowerWind"]


WaveEnergy=Data["WaveEnergy"]
WaveLatLong=Data["WaveLatLong"]
NumWaveSites=WaveEnergy.shape[0]
RatedPowerWave=Data["RatedPowerWave"]
          

OceanEnergy=Data["OceanEnergy"]
OceanEnergy=OceanEnergy[1:100,:]
OceanLatLong=Data["OceanLatLong"]
OceanLatLong=OceanLatLong[1:100,:]
NumOceanSites=OceanEnergy.shape[0]      
RatedPowerOcean=Data["RatedPowerOcean"]

MaximumEnergy=np.dot(Nt,[RatedPowerWind,RatedPowerWave,RatedPowerOcean])

#Eliminate the wind data if the number of wind turbines is zero
if Nt[0]==0:
    WindEnergy=WindEnergy[[],:]
    WindLatLong=WindLatLong[[],:]
    NumWindSites=WindEnergy.shape[0]

#Eliminate the wave data if the number of wave turbines is zero
if Nt[1]==0:
    WaveEnergy=WaveEnergy[[],:]
    WaveLatLong=WaveLatLong[[],:]
    NumWaveSites=WaveEnergy.shape[0]

#Eliminate the ocean current data if the number of ocean current turbines is zero
if Nt[2]==0:
    OceanEnergy=OceanEnergy[[],:]
    OceanLatLong=OceanLatLong[[],:]
    NumOceanSites=OceanEnergy.shape[0]


Nu=np.concatenate((np.full((NumWindSites), NuWiWaOcean[0]),np.full((NumWaveSites), NuWiWaOcean[1]),np.full((NumOceanSites), NuWiWaOcean[2])))

Sigma=np.cov(np.concatenate((WindEnergy,WaveEnergy,OceanEnergy),axis=0))/(10**12) #Variance covariance matrix [MWh**2]
NumSites=Sigma.shape[0]

CF=np.average(np.concatenate((WindEnergy,WaveEnergy,OceanEnergy),axis=0),axis=1)/MaximumEnergy# Capacity factor

#Store set of relaxed solutions 
RelaxedSolutionsCF=[]#Capacity factor
RelaxedSolutionsVar=[]#Variance

OptimalXSolutionsWind=[]
OptimalXSolutionsWave=[]
OptimalXSolutionsOcean=[]
RelaxedSolutionsLatLongWind=[]
RelaxedSolutionsLatLongWave=[]
RelaxedSolutionsLatLongOcean=[]

#Store set of MILP solutions
MILPSolutionsCF=[]
MILPSolutionsVar=[]

OptimalYSolutionsWind=[]
OptimalYSolutionsWave=[]
OptimalYSolutionsOcean=[]
MILPSolutionsLatLongWind=[]
MILPSolutionsLatLongWave=[]
MILPSolutionsLatLongOcean=[]
CFEachOptimalSiteLocationWind=[]
CFEachOptimalSiteLocationWave=[]
CFEachOptimalSiteLocationOcean=[]

#In order to do the optimization process we divided the model in two parts a LP relaxation of the MILP problem and 
#a MILP approximation of the origional MILP, with significanly less integer variables
#
#----------------------------Relaxed optimization model (LP)----------------------------Start
RelaxedMILP = ConcreteModel()

RelaxedMILP.SiteWind = RangeSet(0,NumWindSites-1)# Set of all wind sites
RelaxedMILP.SiteWave = RangeSet(NumWindSites,NumWindSites+NumWaveSites-1)# Set of all wave sites
RelaxedMILP.SiteOcean = RangeSet(NumWindSites+NumWaveSites,NumSites-1)# Set of all ocean current sites

RelaxedMILP.Site = RangeSet(0,NumSites-1)# Set of all sites

RelaxedMILP.x = Var(RelaxedMILP.Site, domain=NonNegativeReals)# x is the number of turbines in each site location

def objective_rule(RelaxedMILP):   
    xtS=[sum(RelaxedMILP.x[i]*Sigma[i,j] for i in RelaxedMILP.Site) for j in RelaxedMILP.Site]
    
    return summation(xtS,RelaxedMILP.x)

RelaxedMILP.OBJ = Objective(rule = objective_rule, sense=minimize)

def NumTurbinesCell_rule(RelaxedMILP,i):
    return RelaxedMILP.x[i]<=Nu[i]

RelaxedMILP.Turbines_Cell = Constraint(RelaxedMILP.Site, rule=NumTurbinesCell_rule)

if NumWindSites!=0:
    RelaxedMILP.TMaxTurbinesWind = Constraint(expr=sum(RelaxedMILP.x[i] for i in RelaxedMILP.SiteWind)==Nt[0])
    
if NumWaveSites!=0:    
    RelaxedMILP.TMaxTurbinesWave = Constraint(expr=sum(RelaxedMILP.x[i] for i in RelaxedMILP.SiteWave)==Nt[1])
    
if NumOceanSites!=0:       
     RelaxedMILP.TMaxTurbinesOcean = Constraint(expr=sum(RelaxedMILP.x[i] for i in RelaxedMILP.SiteOcean)==Nt[2])

opt = SolverFactory('cplex')

IdxLP=[]#Store indexes of all optimal site locations
TrackCF=[]#Track the feasible capacity factors (Constraint: RelaxedMILP.CF_Target)

for CFTarget in CF0:
    
    print("Running Relaxed MILP With CF %.2f" % CFTarget)
    
    RelaxedMILP.CF_Target = Constraint(expr=sum(RelaxedMILP.x[i]*CF[i] for i in RelaxedMILP.Site) >= CFTarget)
    results=opt.solve(RelaxedMILP)

    #Solution in optimal and feasible
    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
 
        Optimal_X=RelaxedMILP.x.get_values()
        
        Optimal_X=np.reshape(np.array([Optimal_X[i] for i in RelaxedMILP.Site]),(1,NumSites))
        
        VarianceLP=float(np.dot(np.dot(Optimal_X,Sigma),Optimal_X.T))#Optimal solution. Minimum variance

        RelaxedSolutionsVar.append(VarianceLP)
        RelaxedSolutionsCF.append(np.sum(Optimal_X*CF))#CF in the optimal solution.
        
        #IdxLP: Indexes good for the MILP phase
        IdxLP.append(np.reshape(np.array([Optimal_X>10**-2]),-1))#For the integer part we only consider site locations with x*>0.01

        if NumWindSites!=0:
            TempXWind=Optimal_X[0, RelaxedMILP.SiteWind]
            IdxLPWind=np.reshape(np.array([TempXWind> 10**-2]),-1)
            OptimalXSolutionsWind.append(TempXWind[IdxLPWind])
            RelaxedSolutionsLatLongWind.append(WindLatLong[IdxLPWind,:])
            
            
        if NumWaveSites!=0:  
            TempXWave=Optimal_X[0, RelaxedMILP.SiteWave]
            IdxLPWave=np.reshape(np.array([TempXWave> 10**-2]),-1)
            OptimalXSolutionsWave.append(TempXWave[IdxLPWave])
            RelaxedSolutionsLatLongWave.append(WaveLatLong[IdxLPWave,:])

        if NumOceanSites!=0:        
            TempXOcean=Optimal_X[0, RelaxedMILP.SiteOcean]
            IdxLPOcean=np.reshape(np.array([TempXOcean> 10**-2]),-1)
            OptimalXSolutionsOcean.append(TempXOcean[IdxLPOcean])
            RelaxedSolutionsLatLongOcean.append(OceanLatLong[IdxLPOcean,:])
            
        
        
        #Delete constraint for its modification in the next step of the for loop
        RelaxedMILP.del_component(RelaxedMILP.CF_Target)
        TrackCF.append(CFTarget)
        
    #elif (results.solver.termination_condition == TerminationCondition.infeasible):#model in infeasible
    else:# Something else is wrong
        RelaxedMILP.del_component(RelaxedMILP.CF_Target)
        if TrackCF!=[]:
            break
#----------------------------Relaxed optimization model (LP)----------------------------End


#----------------------------Approximated MILP----------------------------Start
IdxMILP=[]#Store indexes of all optimal site locations

for CFScenario in range(len(TrackCF)):
    CFTarget=TrackCF[CFScenario]
    
    IdxLPWind=IdxLP[CFScenario][RelaxedMILP.SiteWind]
    IdxLPWave=IdxLP[CFScenario][RelaxedMILP.SiteWave]
    IdxLPOcean=IdxLP[CFScenario][RelaxedMILP.SiteOcean]   

    WindEnergyMILP=WindEnergy[IdxLPWind,:]
    WaveEnergyMILP=WaveEnergy[IdxLPWave,:]
    OceanEnergyMILP=OceanEnergy[IdxLPOcean,:]

    NumWindSites=WindEnergyMILP.shape[0]
    NumWaveSites=WaveEnergyMILP.shape[0]
    NumOceanSites=OceanEnergyMILP.shape[0]   

    Sigma=np.cov(np.concatenate((WindEnergyMILP, WaveEnergyMILP, OceanEnergyMILP),axis=0))/(10**12) #Variance covariance matrix [MWh**2]
    NumSites=Sigma.shape[0]

    CF=np.average(np.concatenate((WindEnergyMILP, WaveEnergyMILP, OceanEnergyMILP),axis=0),axis=1)/MaximumEnergy

    Nu=np.concatenate((np.full((NumWindSites), NuWiWaOcean[0]),np.full((NumWaveSites), NuWiWaOcean[1]),np.full((NumOceanSites), NuWiWaOcean[2])))

    MILP = ConcreteModel()

    MILP.SiteWind = RangeSet(0,NumWindSites-1)
    MILP.SiteWave = RangeSet(NumWindSites,NumWindSites+NumWaveSites-1)
    MILP.SiteOcean = RangeSet(NumWindSites+NumWaveSites,NumSites-1)
    MILP.Site = RangeSet(0,NumSites-1)

    MILP.y = Var(MILP.Site, domain=NonNegativeIntegers)# Integer variable to track the number of turbines used per site location

    MILP.v = Var(MILP.Site, domain=Binary)# Binary variable to track the number of sites used

    def objective_rule(MILP):
        ytS=[sum(MILP.y[i]*Sigma[i,j] for i in MILP.Site) for j in MILP.Site]
        return summation(ytS,MILP.y)

    MILP.OBJ = Objective(rule = objective_rule, sense=minimize)

    MILP.CF_Target = Constraint(expr=sum(MILP.y[i]*CF[i] for i in MILP.Site) >= CFTarget)

    def NumTurbinesCell_rule(MILP,i):
        return MILP.y[i]<=Nu[i]*MILP.v[i]

    MILP.Turbines_Cell = Constraint(MILP.Site, rule=NumTurbinesCell_rule)

    NumWindSites=WindEnergyMILP.shape[0]
    NumWaveSites=WaveEnergyMILP.shape[0]
    NumOceanSites=OceanEnergyMILP.shape[0]   

    if NumWindSites!=0:
        MILP.MaxSiteLocationsWind = Constraint(expr=sum(MILP.v[i] for i in MILP.SiteWind)<=Ns[0])
        MILP.TMaxTurbinesWind = Constraint(expr=sum(MILP.y[i] for i in MILP.SiteWind)==Nt[0])
    
    if NumWaveSites!=0:
        MILP.MaxSiteLocationsWave = Constraint(expr=sum(MILP.v[i] for i in MILP.SiteWave)<=Ns[1])
        MILP.TMaxTurbinesWave = Constraint(expr=sum(MILP.y[i] for i in MILP.SiteWave)==Nt[1])
    
    if NumOceanSites!=0:
        MILP.MaxSiteLocationsOcean = Constraint(expr=sum(MILP.v[i] for i in MILP.SiteOcean)<=Ns[2])
        MILP.TMaxTurbinesOcean = Constraint(expr=sum(MILP.y[i] for i in MILP.SiteOcean)==Nt[2])

    opt = SolverFactory('cplex')
    resultsMILP=opt.solve(MILP)
    
    #solution in optimal and feasible
    if (resultsMILP.solver.status == SolverStatus.ok) and (resultsMILP.solver.termination_condition == TerminationCondition.optimal):
 
        Optimal_Y=MILP.y.get_values()
        
        Optimal_Y=np.reshape(np.array([Optimal_Y[i] for i in MILP.Site]),-1)
        
        VarianceMILP=float(np.dot(np.dot(Optimal_Y,Sigma),Optimal_Y.T))#Optimal solution. Minimum variance

        MILPSolutionsVar.append(VarianceMILP)
        
        MILPSolutionsCF.append(np.sum(Optimal_Y*CF))#CF in the optimal solution.
      
        TempIDX=np.copy(IdxLP[CFScenario])
        TempIDX[TempIDX==1]=np.reshape((Optimal_Y>=1),-1)
        
        if NumWindSites!=0:
            TempYWind=Optimal_Y[MILP.SiteWind]
            OptimalYSolutionsWind.append(TempYWind[TempYWind>=1])
            
            IdxWind=TempIDX[RelaxedMILP.SiteWind]
            MILPSolutionsLatLongWind.append(WindLatLong[IdxWind,:])
            
            CFEachOptimalSiteLocationWind.append(np.average(WindEnergy[IdxWind,:],axis=1)/RatedPowerWind)
            
            
        if NumWaveSites!=0:
            TempYWave=Optimal_Y[MILP.SiteWave]
            OptimalYSolutionsWave.append(TempYWave[TempYWave>=1])
            IdxWave=TempIDX[RelaxedMILP.SiteWave]
            MILPSolutionsLatLongWave.append(WaveLatLong[IdxWave,:])
            
            CFEachOptimalSiteLocationWave.append(np.average(WaveEnergy[IdxWave,:],axis=1)/RatedPowerWave)
            
            
        if NumOceanSites!=0:
            TempYOcean=Optimal_Y[MILP.SiteOcean]            
            OptimalYSolutionsOcean.append(TempYOcean[TempYOcean>=1])     
            IdxOcean=TempIDX[RelaxedMILP.SiteOcean]         
            MILPSolutionsLatLongOcean.append(OceanLatLong[IdxOcean,:])
            
            CFEachOptimalSiteLocationOcean.append(np.average(OceanEnergy[IdxOcean,:],axis=1)/RatedPowerOcean)
              
            
    #elif (resultsMILP.solver.termination_condition == TerminationCondition.infeasible):#model in infeasible
    else:# Something else is wrong
        break
    
elapsed_time = time.time() - start_time
#----------------------------Approximated MILP----------------------------Start

ReadME='\
    1) CfFeasible: CF simulated by the LP problem (Feasible)\n\
    2) CfSimulated: CF simulated by the portfolio optimization (all cases including infeasible ones)\n\
    3) TotalNumTurbines: Total number of turbines (Wind,Wave,Ocean Current)\n\
    4) MaxNumTurbines: Maximum number of turbines per grid cell (Wind,Wave,Ocean Current)\n\
    5) MaxNumSites: Maximum number of site locations (Wind,Wave,Ocean Current)\n\
    6) RelaxedSolutionsCF: Values of CF for the portfolios in the relaxed MILP (after optimization)\n\
    7) RelaxedSolutionsVar: Values of variance for the portfolios in the relaxed MILP\n\
    8) OptimalXSolutionsWind: Number of wind turbines in each optimal site location for the relaxed MILP\n\
    9) OptimalXSolutionsWave: Number of wave turbines in each optimal site location for the relaxed MILP\n\
    10) OptimalXSolutionsOcean: Number of ocean current turbines in each optimal site location for the relaxed MILP\n\
    11) RelaxedSolutionsLatLongWind: LatLong of each optimal wind site location for the relaxed MILP\n\
    12) RelaxedSolutionsLatLongWave: LatLong of each optimal wave site location for the relaxed MILP\n\
    13) RelaxedSolutionsLatLongOcean: LatLong of each optimal ocean current site location for the relaxed MILP\n\
    14) MILPSolutionsCF: Values of CF for the portfolios in the  MILP (after optimization)\n\
    15) MILPSolutionsVar: Values of variance for the portfolios in the MILP\n\
    16) OptimalYSolutionsWind: Number of wind turbines in each optimal site location for the MILP\n\
    17) OptimalYSolutionsWave: Number of wave turbines in each optimal site location for the MILP\n\
    18) OptimalYSolutionsOcean: Number of ocean current turbines in each optimal site location for the MILP\n\
    19) MILPSolutionsLatlongWind: LatLong of each optimal wind site location for the MILP\n\
    20) MILPSolutionsLatlongWave: LatLong of each optimal wave site location for the MILP\n\
    21) MILPSolutionsLatlongOcean: LatLong of each optimal ocean current site location for the MILP\n\
    22) TotalSimulationTime= Total processing time \n\
    23) CF_EachOptimalSiteLocationWind=  Average CF for each optimal wind site location\n\
    24) CF_EachOptimalSiteLocationWave=  Average CF for each optimal wave site location\n\
    25) CF_EachOptimalSiteLocationOcean= Average CF for each optimal ocean current site location'
    

np.savez("PortlofioOPT1.npz",ReadME=ReadME, CfFeasible=TrackCF, CfSimulated=CF0, TotalNumTurbines=Nt,MaxNumTurbines=NuWiWaOcean, 
         MaxNumSites=Ns, RelaxedSolutionsCF=RelaxedSolutionsCF, RelaxedSolutionsVar=RelaxedSolutionsVar,
         OptimalXSolutionsWind=OptimalXSolutionsWind, OptimalXSolutionsWave=OptimalXSolutionsWave, 
         OptimalXSolutionsOcean=OptimalXSolutionsOcean, RelaxedSolutionsLatLongWind=RelaxedSolutionsLatLongWind,
         RelaxedSolutionsLatLongWave=RelaxedSolutionsLatLongWave, RelaxedSolutionsLatLongOcean=RelaxedSolutionsLatLongOcean,         
         MILPSolutionsCF=MILPSolutionsCF, MILPSolutionsVar=MILPSolutionsVar, OptimalYSolutionsWind=OptimalYSolutionsWind,
         OptimalYSolutionsWave=OptimalYSolutionsWave, OptimalYSolutionsOcean=OptimalYSolutionsOcean, 
         MILPSolutionsLatLongWind=MILPSolutionsLatLongWind, MILPSolutionsLatLongWave=MILPSolutionsLatLongWave,
         MILPSolutionsLatLongOcean=MILPSolutionsLatLongOcean, TotalSimulationTime=elapsed_time,
         CF_EachOptimalSiteLocationWind=CFEachOptimalSiteLocationWind,
         CF_EachOptimalSiteLocationWave=CFEachOptimalSiteLocationWave,
         CF_EachOptimalSiteLocationOcean=CFEachOptimalSiteLocationOcean)
