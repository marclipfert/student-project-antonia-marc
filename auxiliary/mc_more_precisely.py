import pandas as pd
import numpy as np
import statsmodels.formula.api as smf


#****************************************************************************************
#********************* COMPUTING MONTH OF CONCEPTION MORE PRECISELY *********************
#****************************************************************************************

# Create month of birth variable based on month of policy intervention in July 2007
def mc_more_precisely():
    dfb = pd.read_stata('data/data_births_20110196.dta')
    dfb['m'] = 500 # create the variable (in the end no 500 will be left)
    for i in range(11):
        dfb.loc[dfb['year'] == 2000 + i,'m'] = dfb['mesp'] - 91 + 12*i


######################### THIS PART IS THE IMPORTANT ONE ################################
    
    # create the variable
    dfb['mc'] = np.nan
    
    # compute month of conception using information about #-of weeks of pregancy (semanas)
    dfb.loc[(0 < dfb['semanas']) & (dfb['semanas'] <= 21), 'mc'] = dfb['m'] - 4
    dfb.loc[(21 < dfb['semanas']) & (dfb['semanas'] <= 25), 'mc'] = dfb['m'] - 5
    dfb.loc[(25 < dfb['semanas']) & (dfb['semanas'] <= 29), 'mc'] = dfb['m'] - 6
    dfb.loc[(29 < dfb['semanas']) & (dfb['semanas'] <= 34), 'mc'] = dfb['m'] - 7
    dfb.loc[(34 < dfb['semanas']) & (dfb['semanas'] <= 38), 'mc'] = dfb['m'] - 8
    dfb.loc[(38 < dfb['semanas']) & (dfb['semanas'] <= 43), 'mc'] = dfb['m'] - 9
    dfb.loc[43 < dfb['semanas'], 'mc'] = dfb['m'] - 10
    
    # if semanas is missing: approximate mc using premature baby indicator (like the author)
    dfb.loc[(np.isnan(dfb['semanas']) | (0 == dfb['semanas'])) & (dfb['prem'] == 1), 'mc'] = dfb['m'] - 9
    dfb.loc[(np.isnan(dfb['semanas']) | (0 == dfb['semanas'])) & (dfb['prem'] == 2), 'mc'] = dfb['m'] - 8
    
##########################################################################################


# GROUP DATA
    dfb['n'] = 1  # this variable will indicate the number of conception per month
    dfb = dfb.groupby('mc', as_index = False)['n'].count()

    # calendar month of conception
    dfb['month'] = 0
    for i in range(4): #note that range starts at 0 but does not include the last number
        dfb.loc[dfb['mc'] == 0 + 12*i, 'month'] = 7
        dfb.loc[dfb['mc'] == 1 + 12*i, 'month'] = 8
        dfb.loc[dfb['mc'] == 2 + 12*i, 'month'] = 9
        dfb.loc[dfb['mc'] == 3 + 12*i, 'month'] = 10
        dfb.loc[dfb['mc'] == 4 + 12*i, 'month'] = 11
        dfb.loc[dfb['mc'] == 5 + 12*i, 'month'] = 12
        dfb.loc[dfb['mc'] == 6 + 12*i, 'month'] = 1
        dfb.loc[dfb['mc'] == 7 + 12*i, 'month'] = 2
        dfb.loc[dfb['mc'] == 8 + 12*i, 'month'] = 3
        dfb.loc[dfb['mc'] == 9 + 12*i, 'month'] = 4
        dfb.loc[dfb['mc'] == 10 + 12*i, 'month'] = 5
        dfb.loc[dfb['mc'] == 11 + 12*i, 'month'] = 6
    for i in range(9):
        dfb.loc[dfb['mc'] == -1 - 12*i, 'month'] = 6
        dfb.loc[dfb['mc'] == -2 - 12*i, 'month'] = 5
        dfb.loc[dfb['mc'] == -3 - 12*i, 'month'] = 4
        dfb.loc[dfb['mc'] == -4 - 12*i, 'month'] = 3
        dfb.loc[dfb['mc'] == -5 - 12*i, 'month'] = 2
        dfb.loc[dfb['mc'] == -6 - 12*i, 'month'] = 1
        dfb.loc[dfb['mc'] == -7 - 12*i, 'month'] = 12
        dfb.loc[dfb['mc'] == -8 - 12*i, 'month'] = 11
        dfb.loc[dfb['mc'] == -9 - 12*i, 'month'] = 10
        dfb.loc[dfb['mc'] == -10 - 12*i, 'month'] = 9
        dfb.loc[dfb['mc'] == -11 - 12*i, 'month'] = 8
        dfb.loc[dfb['mc'] == -12 - 12*i, 'month'] = 7
        # one can check that no zero is left
    
    # generate July indicator
    dfb['july'] = np.where(dfb['month'] == 7, 1, 0)
    
    # generate number of days in a month
                # leap years from 2000 - 2010: 2008, 2004, 2000
                # --> mc = 7, 7-12*4 = -41, 7-12*8 = -89
    dfb['days'] = np.where((dfb['mc'] == 7) | (dfb['mc'] == -41) | (dfb['mc'] == -89), 29,
        # for all other feburarys
        np.where(dfb['month'] == 2, 28,
        # for April, June, September, November
        np.where((dfb['month'] == 4) | (dfb['month'] == 6) |
                (dfb['month'] == 9) | (dfb['month'] == 11), 30,
                 # otherwise
                 31)))

    # indicator for treatment group (post-policy conception), i.e. after June 2007
    dfb['post'] = np.where(dfb['mc'] >= 0, 1, 0)


    # quadratic and cubic mc
    dfb['mc2'] = dfb['mc']*dfb['mc']
    dfb['mc3'] = dfb['mc']*dfb['mc']*dfb['mc']

    # natural log of number of obs n
    dfb['ln'] = np.log(dfb['n'])

    # get month dummies
    dummies = pd.get_dummies(dfb['month'])
    dummies.columns = ['jan','feb','mar','apr','mai','jun','jul','aug','sep','oct','nov','dec']
    # bind data frames
    dfb = pd.concat([dfb, dummies], axis=1)
   
    
    return dfb



# *********************************** CONCEPTIONS - REGRESSIONS **********************************


def table_reg_output_2(reg_output1, reg_output2):
    
    # Make a table equivalent to Table 2 with coefficients and se for post variable
    print('\u2014'*110)
    # header
    print('{:<12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'
          .format("", "RDD (1)", "RDD (2)", "RDD (3)", "RDD (4)", "RDD (5)", "DID (6)", "DID (7)", "DID (8)"))
    print('{:<12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'
          .format("", "10 years", "5 years", "12 months", "9 months", "3 months", "10 years", "7 years", "5 years"))
    print('\u2014'*110)
    
    # REG OUTPUT 1
    print('{:<12s}'.format("mc revised"), end="")
    # coefficient estimate
    for i in range(len(reg_output1)):
        print ('{:>12.4f}'.format(reg_output1[i].params.post), end="")
    # standard error
    print(" "*110)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output1)):
        print ('{:>12.4f}'.format(reg_output1[j].bse.post), end="")
    # p-value
    print(" "*110)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output1)):
        print ('\033[1m' '{:>12.4f}' '\033[0m'.format(reg_output1[j].pvalues.post), end="")
    
    # REG OUTPUT 2
    print(" "*110)
    print('{:<12s}'.format("mc old"), end="")
    # coefficient estimate
    for i in range(len(reg_output2)):
        print ('{:>12.4f}'.format(reg_output2[i].params.post), end="")
    # standard error
    print(" "*110)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output2)):
        print ('{:>12.4f}'.format(reg_output2[j].bse.post), end="")
    # p-value
    print(" "*110)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output2)):
        print ('\033[1m' '{:>12.4f}' '\033[0m'.format(reg_output2[j].pvalues.post), end="")

    
 