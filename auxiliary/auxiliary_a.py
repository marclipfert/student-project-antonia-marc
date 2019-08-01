import pandas as pd
import numpy as np
import statsmodels.formula.api as smf


#****************************************************************************************
#********************** DATA PROCESSING BASED ON dofile_fertility ***********************
#****************************************************************************************

#************************************** CONCEPTIONS *************************************

# Create month of birth variable based on month of policy intervention in July 2007
def gen_var_m():
    dfb = pd.read_stata('data/data_births_20110196.dta')
    dfb['m'] = 500 # create the variable (in the end no 500 will be left)
    for i in range(11):
        dfb.loc[dfb['year'] == 2000 + i,'m'] = dfb['mesp'] - 91 + 12*i
    return dfb


# Create month of conception variable mc3
def gen_var_mc():
    dfb = gen_var_m()
    dfb['mc'] = np.where((dfb['prem'] == 2) |
        # if premature baby subtract only 8 months to get month of conception
        ((0 < dfb['semanas']) & (dfb['semanas'] < 39)), dfb['m'] - 8,
        # otherwise if baby was born only after 43 months --> -10
        np.where(dfb['semanas'] > 43, dfb['m'] - 10,
        # otherwise --> - 9
        dfb['m'] - 9))
    return dfb



# GROUP DATA
def group_data():
    dfb = gen_var_mc()
    dfb['n'] = 1  # this variable will indicate the number of conception per month
    dfb = dfb.groupby('mc', as_index = False)['n'].count()
    return dfb


def complete_processing_conceptions_data():
    dfb = group_data()
    
    # calendar month of conception
    dfb['month'] = 0
    for i in range(3): #note that range starts at 0 but does not include the last number
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
    
    # store final births data set
    dfb.to_pickle('data/dfb.pkl')
    
    return dfb



        
#************************************** ABORTIONS ********************************************

def process_abortions_data():
    dfa = pd.read_stata('data/data_abortions_20110196.dta')

    # Variables:
    # n_ive_and "Number of abortions per month in Andalucia, 1999-2009"
    # n_ive_val "Number of abortions per month in C. Valenciana, 2000-2010"
    # n_ive_rioja "Number of abortions per month in La Rioja, 2000-2009"
    # n_ive_cat "Number of abortions per month in Cataluña, 2000-2009"
    # n_ive_can "Number of abortions per month in Canarias, 1999-2010"
    # n_ive_mad "Number of abortions per month in Madrid, 1999-2009"
    # n_ive_gal "Number of abortions per month in Galicia, 2000-2009"
    # n_ive_bal "Number of abortions per month in Baleares, 2000-2009"
    # n_ive_pv "Number of abortions per month in Pais Vasco, 2000-2009"
    # n_ive_castlm "Number of abortions per month in Castilla La Mancha, 2000-2010"
    # n_ive_ast "Number of abortions per month in Asturias, 2000-2010"
    # n_ive_arag "Number of abortions per month in Aragon, 2000-2010"

    
    # sum of abortions across all regions
    dfa['n_tot'] = dfa.iloc[:,2:14].sum(axis=1)  # 2:14 chooses columns 3 to 14

    # month variable that takes value 0 in July 2007:
    # (the data is already sorted and there is only one observation per month and year)
    dfa['m'] = range(len(dfa))
    dfa['m'] = dfa['m'] - 102  # the value for July 2007 is changed from 102 to 0, other variable entries respectively

    # days in a month:
    dfa['days'] = np.where((dfa['month'] == 2) & ((dfa['year'] == 2000) | (dfa['year'] == 2004) | (dfa['year'] == 2008)), 29,
            # for all other feburarys
            np.where(dfa['month'] == 2, 28,
            # for April, June, September, November
            np.where((dfa['month'] == 4) | (dfa['month'] == 6) |
                    (dfa['month'] == 9) | (dfa['month'] == 11), 30,
            # otherwise
            31)))

    # log-abortions
    dfa['log_ive'] = np.log(dfa['n_tot'])
    
    # squared and cubed terms
    dfa['m2'] = dfa['m']*dfa['m']
    dfa['m3'] = dfa['m']*dfa['m']*dfa['m']
    
    # post indicator
    dfa['post'] = np.where(dfa['m'] >= 0, 1, 0)
    
    # restrict period
    dfa = dfa.loc[(dfa['m']> -91) & (dfa['m']<30)]
    
    # get month dummies
    dummies = pd.get_dummies(dfa['month'])
    dummies.columns = ['jan','feb','mar','apr','mai','jun','jul','aug','sep','oct','nov','dec']
    # bind data frames
    dfa = pd.concat([dfa, dummies], axis=1)
    
    # store final abortions data set
    dfa.to_pickle('data/dfa.pkl')
    
    return dfa





# *********************************** CONCEPTIONS - REGRESSIONS **********************************


def reg_conception(data_frame):
    
    # create necessary subsets of data_frame
    dfb_list = list()

    dfb_list.append(data_frame.loc[(data_frame['mc']>-91) & (data_frame['mc']<30)]) # 10 years
    dfb_list.append(data_frame.loc[(data_frame['mc']>-31) & (data_frame['mc']<30)]) # 5 years
    dfb_list.append(data_frame.loc[(data_frame['mc']>-13) & (data_frame['mc']<12)]) # 12 months
    dfb_list.append(data_frame.loc[(data_frame['mc']>-10) & (data_frame['mc']<9)]) # 9 months
    dfb_list.append(data_frame.loc[(data_frame['mc']>-4) & (data_frame['mc']<3)]) # 3 months
    dfb_list.append(data_frame.loc[(data_frame['mc']>-67) & (data_frame['mc']<30)]) # 8 years
    
    # regress
    reg1 = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + mc3 + post*mc3 + days', data=dfb_list[0]).fit(cov_type='HC1')
    reg2 = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + days', data=dfb_list[1]).fit(cov_type='HC1')
    reg3 = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + days', data=dfb_list[2]).fit(cov_type='HC1')
    reg4 = smf.ols(formula =
            'ln ~ post + mc + post*mc + days', data=dfb_list[3]).fit(cov_type='HC1')
    reg5 = smf.ols(formula =
            'ln ~ post + days', data=dfb_list[4]).fit(cov_type='HC1')
    reg6 = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + mc3 + post*mc3 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfb_list[0]).fit(cov_type='HC1')
    reg7 = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfb_list[5]).fit(cov_type='HC1')
    reg8 = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfb_list[1]).fit(cov_type='HC1')
    
    # store regression results in list
    reg_list_b = [reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8]

       
    return reg_list_b
 

    
#******************************* REGRESSIONS ABORTIONS ****************************************

def reg_abortion(data_frame):
        
    # create necessary subsets of data_frame
    dfa_list = list()

    # same subsets as for births data set
    dfa_list.append(data_frame.loc[(data_frame['m']>-91) & (data_frame['m']<30)]) # 10 years
    dfa_list.append(data_frame.loc[(data_frame['m']>-31) & (data_frame['m']<30)]) # 5 years
    dfa_list.append(data_frame.loc[(data_frame['m']>-13) & (data_frame['m']<12)]) # 12 months
    dfa_list.append(data_frame.loc[(data_frame['m']>-10) & (data_frame['m']<9)]) # 9 months
    dfa_list.append(data_frame.loc[(data_frame['m']>-4) & (data_frame['m']<3)]) # 3 months
    dfa_list.append(data_frame.loc[(data_frame['m']>-67) & (data_frame['m']<30)]) # 8 years


    reg1 = smf.ols(formula =
            'log_ive ~ post + m + post*m + m2 + post*m2 + m3 + post*m3 + days', data=dfa_list[0]).fit(cov_type='HC1')
    reg2 = smf.ols(formula =
            'log_ive ~ post + m + post*m + m2 + post*m2 + days', data=dfa_list[1]).fit(cov_type='HC1')
    reg3 = smf.ols(formula =
            'log_ive ~ post + m + post*m + m2 + post*m2 + days', data=dfa_list[2]).fit(cov_type='HC1')
    reg4 = smf.ols(formula =
            'log_ive ~ post + m + post*m + days', data=dfa_list[3]).fit(cov_type='HC1')
    reg5 = smf.ols(formula =
            'log_ive ~ post + days', data=dfa_list[4]).fit(cov_type='HC1')
    reg6 = smf.ols(formula =
            'log_ive ~ post + m + post*m + m2 + post*m2 + m3 + post*m3 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfa_list[0]).fit(cov_type='HC1')
    reg7 = smf.ols(formula =
            'log_ive ~ post + m + post*m + m2 + post*m2 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfa_list[5]).fit(cov_type='HC1')
    reg8 = smf.ols(formula =
            'log_ive ~ post + m + post*m + m2 + post*m2 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfa_list[1]).fit(cov_type='HC1')

    reg_list_a = [reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8]
 
    
    return reg_list_a
    
    

    
# ************************************** REGRESSION OUTPUT - TABLE **********************************


# function creating significance stars:
def star_function(p):
    if(round(p,10) <= 0.01):
        star = "***"
    elif round(p,10) <= 0.05:
        star = "**"
    elif round(p,10) <= 0.1:
        star = "*"
    else:
        star = " "
    
    return star

def table_reg_output(reg_output1, reg_output2):
    
    # Make a table equivalent to Table 2 with coefficients and se for post variable
    print('Table 3 - Fertility Results (Conceptions and Abortions)')
    print('\u2014'*116)
    # header
    print('{:<12s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}'
          .format("", "RDD (1)", "", "RDD (2)", "", "RDD (3)", "", "RDD (4)", "", "RDD (5)", "", "DID (6)", "", \
                  "DID (7)", "", "DID (8)", ""))
    print('{:<12s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}{:>10s}{:<3s}'
          .format("", "10 years", "", "5 years", "", "12 months", "", "9 months", "", "3 months", "", "10 years", "", \
                  "7 years", "", "5 years", ""))
    print('\u2014'*116)
    
    # REG OUTPUT 1
    print('{:<12s}'.format("Conceptions"), end="")
    # coefficient estimate
    for i in range(len(reg_output1)):
        print ('{:>10.4f}{:<3s}'.format(reg_output1[i].params.post, star_function(reg_output1[i].pvalues.post)), end="")
    # standard error
    print(" "*116)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output1)):
        print ('\33[34m''{:>10.4f}{:<3s}' '\33[0m'.format(reg_output1[j].bse.post, ""), end="")
    # p-value
    print(" "*116)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output1)):
        print ('\33[31m' '{:>10.4f}{:<3s}' '\33[0m'.format(reg_output1[j].pvalues.post, ""), end="")
    
    # REG OUTPUT 2
    print(" "*116)
    print(" "*116)
    print('{:<12s}'.format("Abortions"), end="")
    # coefficient estimate
    for i in range(len(reg_output2)):
        print ('{:>10.4f}{:<3s}'.format(reg_output2[i].params.post, star_function(reg_output2[i].pvalues.post)), end="")
    # standard error
    print(" "*116)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output2)):
        print ('\33[34m''{:>10.4f}{:<3s}' '\33[0m'.format(reg_output2[j].bse.post, ""), end="")
    # p-value
    print(" "*116)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_output2)):
        print ('\33[31m' '{:>10.4f}{:<3s}' '\33[0m'.format(reg_output2[j].pvalues.post, ""), end="")
    
    #footer
    print(" "*116)
    print('\u2014'*116)
    print("Notes: The dependent variables are the natural logarithm of the monthly number of conceptions and abortions,")
    print("respectively. For each of them, the coefficient, standard error, and p-value of the binary treatment indicator")
    print("variable is reported.")
    print ('- coefficient estimates')
    print ('\33[34m' '- standard errors' '\33[0m')
    print ('\33[31m' '- p-values' '\33[0m')
    
    
        

    
