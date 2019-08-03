
#*************************** SMALL SIMULATION STUDY *****************************
#************* TIME-VARYING TREATMENT: MOVE UP CONCEPTIONS IN TIME **************

import numpy as np
import pandas as pd
import math as math
import statsmodels.formula.api as smf
import scipy.stats as ss

def simulating_results_from_different_bandwidths(running, dummy, treatment, N):
    # create empty arrays to store results inside
    params = np.zeros((5,N), np.float)
    bse = np.zeros((5,N), np.float)
    in_ci = np.zeros((5,N), np.float)
    
    # quantile for 95% confidence interval
    q = ss.norm.ppf(0.975)
    
    for n in range(N):
        
        y = 20 + 0.05*running + treatment + np.random.normal(0, 0.5, len(running))
    
        df = pd.DataFrame(data = {'y': y, 'z': running, 'D': dummy})
    
        reg1 = smf.ols(formula = 'y ~ z + D + D*z', data = df).fit(cov_type='HC1')
        reg2 = smf.ols(formula = 'y ~ z + D + D*z', data = df.loc[(df['z']>-31) & (df['z']<30)]).fit(cov_type='HC1')
        reg3 = smf.ols(formula = 'y ~ z + D + D*z', data = df.loc[(df['z']>-13) & (df['z']<12)]).fit(cov_type='HC1')
        reg4 = smf.ols(formula = 'y ~ z + D + D*z', data = df.loc[(df['z']>-10) & (df['z']<9)]).fit(cov_type='HC1')
        reg5 = smf.ols(formula = 'y ~ D', data = df.loc[(df['z']>-4) & (df['z']<3)]).fit(cov_type='HC1')
        reg_list = [reg1, reg2, reg3, reg4, reg5]
        
        ci_lower = [0, 0, 0, 0, 0]
        ci_upper = [0, 0, 0, 0, 0]
        
        for i in range(5):
            
            params[i,n] = reg_list[i].params['D']
            bse[i,n] = reg_list[i].bse['D']
            
            ci_lower[i] = reg_list[i].params['D'] - q*reg_list[i].bse['D']
            ci_upper[i] = reg_list[i].params['D'] + q*reg_list[i].bse['D']
            
            if ci_lower[i] <= 0 <= ci_upper[i]:
                in_ci[i, n] = 1
            else:
                in_ci[i, n] = 0
    
    return params, bse, in_ci



# Print results

def print_simulation_results(params, bse, in_ci, N):
    print('Simulation Study - Results')
    print('\u2014'*100)
    # header
    print('{:<22s}{:>14s}{:>14s}{:>14s}{:>14s}{:>14s}'
          .format("", "RDD (1)", "RDD (2)", "RDD (3)", "RDD (4)", "RDD (5)"))
    print('{:<22s}{:>14s}{:>14s}{:>14s}{:>14s}{:>14s}'
              .format("", "10 years", "5 years", "12 months", "9 months", "3 months"))
    print('\u2014'*100)
    
    # Average coefficient
    print('{:<25s}'.format("Estimated Coef. of D"), end="")
        # coefficient estimate
    for i in range(len(params)):
        print ('{:>10.4f}'.format(params[i,:].mean()), end="    ")
    print(" "*116)
    
    # Average coefficient
    print('{:<25s}'.format("Standard Error"), end="")
        # coefficient estimate
    for i in range(len(params)):
        print ('{:>10.4f}'.format(bse[i,:].mean()), end="    ")
    print(" "*116)
    
    # Average coefficient
    print('{:<25s}'.format("0 in 0.95-Conf. Int."), end="")
        # coefficient estimate
    for i in range(len(params)):
        print ('{:>10.4f}'.format(sum(in_ci[i,:])/N ), end="    ")
    print(" "*116)
    print('\u2014'*100)
    
    print('The first row contains the average of the estimated coefficient of D. The second row contains the')
    print('average of the corresponding standard error. The last row shows the relative frequency of the event')
    print('that 0 (the overall effect) was included in the 95%-confidence interval.')



# increase timespan

def increase_available_timespan(t_max):
    z_ = np.linspace(-90, t_max, num = (t_max + 91), dtype = int)
    D_ = np.where(z_ < 0, 0, 1)
    sin_ = np.zeros(len(z_))
    for i in z_:
        sin_[i] = math.sin(0.5*z_[i])
    
    T_ = np.where( (z_ < 0) | (z_ > 4*math.pi), 0, sin_)
    
    N_ = 1000
    params_ = np.zeros(N_, np.float)
    bse_ = np.zeros(N_, np.float)
    in_ci_ = np.zeros(N_, np.float)
    q_ = ss.norm.ppf(0.975)
    
    for n in range(N_):
        
        y_ = 20 + 0.05*z_ + T_ + np.random.normal(0, 0.5, len(z_))
    
        df_ = pd.DataFrame(data = {'y': y_, 'z': z_, 'D': D_})
    
        reg = smf.ols(formula = 'y_ ~ z_ + D_ + D_*z_', data = df_).fit(cov_type='HC1')
        
        ci_lower = []
        ci_upper = []
        
        params_[n] = reg.params['D_']
        bse_[n] = reg.bse['D_']
            
        ci_lower = reg.params['D_'] - q_*reg.bse['D_']
        ci_upper = reg.params['D_'] + q_*reg.bse['D_']
            
        if ci_lower <= 0 <= ci_upper:
            in_ci_[n] = 1
        else:
            in_ci_[n] = 0
    
    return params_