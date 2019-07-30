import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt


#****************************************************************************************
#********************************** FUNCTIONS FOR PLOTS *********************************
#****************************************************************************************

def RDD_plot_conceptions(dataframe, reg_output):
    
    # create necessary subsets according to Figure 1. Fertility Effect (paper)
    dfb_subset = dataframe.loc[(dataframe['mc']>-31) & (dataframe['mc']<21)]
    dfb_subset_y0 = dataframe.loc[(dataframe['mc']>-31) & (dataframe['mc']<0)]
    dfb_subset_y1 = dataframe.loc[(dataframe['mc']>=0) & (dataframe['mc']<21)]
    
    if len(reg_output.params) == 7:
        # get coefficients from: ln ~ post + mc + post*mc + mc2 + post*mc2 + days    
        # compute fitted values for both treatment groups
        
        b_fit_y0 = reg_output.params[0] + reg_output.params[2]*dfb_subset_y0['mc'] + reg_output.params[4]*dfb_subset_y0['mc2'] + reg_output.params[6]*dfb_subset_y0['days']
        
        b_fit_y1 = reg_output.params[0] + reg_output.params[1]*dfb_subset_y1['post'] + reg_output.params[2]*dfb_subset_y1['mc'] + reg_output.params[3]*dfb_subset_y1['post']*dfb_subset_y1['mc'] + reg_output.params[4]*dfb_subset_y1['mc2'] + reg_output.params[5]*dfb_subset_y1['post']*dfb_subset_y1['mc2'] + reg_output.params[6]*dfb_subset_y1['days']
        
    
    if len(reg_output.params) == 4:
        # get coefficients from: ln ~ post + mc + post*mc
        # compute fitted values for both treatment groups
        b_fit_y0 = reg_output.params[0] + reg_output.params[2]*dfb_subset_y0['mc']
        
        b_fit_y1 = reg_output.params[0] + reg_output.params[1]*dfb_subset_y1['post'] + reg_output.params[2]*dfb_subset_y1['mc'] + reg_output.params[3]*dfb_subset_y1['post']*dfb_subset_y1['mc']
    
    
    # define colors
    b_col = np.where(dfb_subset['month'] == 7,'r','k')
    
    # plot
    dfb_subset.plot(x='mc',y='ln',kind="scatter",ylim=(10.45,10.8), color = b_col)
    plt.plot(dfb_subset_y0['mc'], b_fit_y0, dfb_subset_y1['mc'], b_fit_y1)
    plt.axvline(x = -0.5, color="b")
    plt.title('Natural logarithm of Number of Conceptions per Month')
    plt.show()

    
    
def RDD_plot_abortions(dataframe, reg_output):
    
    # create necessary subsets according to Figure 1. Fertility Effect (paper)
    dfa_subset = dataframe.loc[(dataframe['m']>-31) & (dataframe['m']<21)]
    dfa_subset_y0 = dataframe.loc[(dataframe['m']>-31) & (dataframe['m']<0)]
    dfa_subset_y1 = dataframe.loc[(dataframe['m']>=0) & (dataframe['m']<21)]
    
    if len(reg_output.params) == 7:
        # get coefficients from: log_ive ~ post + m + post*m + m2 + post*m2 + days 
        # compute fitted values for both treatment groups
        
        a_fit_y0 = reg_output.params[0] + reg_output.params[2]*dfa_subset_y0['m'] + reg_output.params[4]*dfa_subset_y0['m2'] + reg_output.params[6]*dfa_subset_y0['days']
        
        a_fit_y1 = reg_output.params[0] + reg_output.params[1]*dfa_subset_y1['post'] + reg_output.params[2]*dfa_subset_y1['m'] + reg_output.params[3]*dfa_subset_y1['post']*dfa_subset_y1['m'] + reg_output.params[4]*dfa_subset_y1['m2'] + reg_output.params[5]*dfa_subset_y1['post']*dfa_subset_y1['m2'] + reg_output.params[6]*dfa_subset_y1['days']
        
    
    if len(reg_output.params) == 4:
        # get coefficients from: log_ive ~ post + m + post*m 
        # compute fitted values for both treatment groups
        
        a_fit_y0 = reg_output.params[0] + reg_output.params[2]*dfa_subset_y0['m']
        
        a_fit_y1 = reg_output.params[0] + reg_output.params[1]*dfa_subset_y1['post'] + reg_output.params[2]*dfa_subset_y1['m'] + reg_output.params[3]*dfa_subset_y1['post']*dfa_subset_y1['m']
    
    
    # define colors
    a_col = np.where(dfa_subset['month'] == 7,'r','k')
    
    # plot
    dfa_subset.plot(x='m',y='log_ive',kind="scatter",ylim=(8.6,9.4), color = a_col)
    plt.plot(dfa_subset_y0['m'], a_fit_y0, dfa_subset_y1['m'], a_fit_y1)
    plt.axvline(x = -0.5, color="b")
    plt.title('Natural logarithm of Number of Abortions per Month')
    plt.show()
