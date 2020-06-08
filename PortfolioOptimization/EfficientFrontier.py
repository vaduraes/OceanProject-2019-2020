#Plot Efficient Frontier of the data in "Portfolio"

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as Inp
import scipy

Portfolio=np.load("PortfolioOptimizationWindWaveOcean(0_100_0).npz",allow_pickle=True)

LCOE_Stage1=Portfolio['RelaxedSolutionsLCOE']
Std_Stage1=Portfolio['RelaxedSolutionsVar']
#in some simulations I forgot to multiply the rated power by 10^-6

LCOE_Stage1=LCOE_Stage1[LCOE_Stage1!=None]
Std_Stage1=Std_Stage1[(Std_Stage1!=None)]

Std_Stage1=(Std_Stage1)**(1/2)


LCOE_Stage2=Portfolio['MINLPSolutionsLCOE']
Std_Stage2=Portfolio['MINLPSolutionsVar']

LCOE_Stage2=LCOE_Stage2[LCOE_Stage2!=None]
Std_Stage2=Std_Stage2[(Std_Stage2!=None)]

Std_Stage2=Std_Stage2**(1/2)


plt.plot(Std_Stage1, LCOE_Stage1, c='b',linestyle='-', label='Stage 1')
plt.plot(Std_Stage2, LCOE_Stage2, c='r', label='Stage 2')

plt.legend()
plt.title('Efficient Frontier- 0 Wind 100 Wave 0 Ocean')
plt.xlabel('\u03C3')
plt.ylabel('LCOE [$/MWh]')
plt.savefig('Efficient Frontier 0_100_0 ', dpi=700)
plt.close()  