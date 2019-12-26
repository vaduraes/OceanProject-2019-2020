#Graph variance X capacity factor
import numpy as np
import matplotlib.pyplot as plt

OptimizationResults=np.load('PortlofioOPT1.npz')#Results from the portfolio optimization

RelaxedSolutionsCF=OptimizationResults['RelaxedSolutionsCF']*100
RelaxedSolutionsVar=OptimizationResults['RelaxedSolutionsVar']

MILPSolutionsCF=OptimizationResults['MILPSolutionsCF']*100
MILPSolutionsVar=OptimizationResults['MILPSolutionsVar']

fig= plt.plot()

plt.plot(RelaxedSolutionsVar, RelaxedSolutionsCF, 'go--', linewidth=2, markersize=7,label='Stage 1')
plt.plot(MILPSolutionsVar, MILPSolutionsCF, 'bo--', linewidth=2, markersize=7,label='Stage 2')

plt.legend()

plt.ylabel("Capacity Factor (%)")
plt.xlabel("Variance [MWh²]")


plt.title("Variance X CF")

plt.savefig('VarianceXCF',dpi=700)