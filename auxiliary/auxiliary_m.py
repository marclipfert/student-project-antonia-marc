import pandas as pd
import numpy as np
import statsmodels.formula.api as smf


#******************************************************************************
#********************** DATA PROCESSING BASED ON dofile_hbs *******************
#******************************************************************************



# reading in data set hbs and processing it:

def read_and_manipulate_hbs():
    
    # read in data:
    df_hbs = pd.read_stata('data/data_hbs_20110196.dta')
    
    # age of mom and dad
    df_hbs.loc[df_hbs['agemom'].isna(), 'agemom'] = 0
    df_hbs.loc[df_hbs['agedad'].isna(), 'agedad'] = 0
    
    # mom or dad not present
    df_hbs.loc[:,['nomom','nodad']] = 0
    df_hbs.loc[df_hbs['agemom'] == 0, 'nomom'] = 1
    df_hbs.loc[df_hbs['agedad'] == 0, 'nodad'] = 1
    
    # education of mom and dad
    df_hbs['sec1mom']=0
    df_hbs['sec1dad']=0

    df_hbs['sec2mom']=0
    df_hbs['sec2dad']=0

    df_hbs['unimom']=0
    df_hbs['unidad']=0

    df_hbs.loc[df_hbs['educmom'] == 3, 'sec1mom'] = 1
    df_hbs.loc[df_hbs['educdad'] == 3, 'sec1dad'] = 1

    df_hbs.loc[(df_hbs['educmom'] > 3) & (df_hbs['educmom']<7), 'sec2mom'] = 1
    df_hbs.loc[(df_hbs['educdad'] > 3) & (df_hbs['educdad']<7), 'sec2dad'] = 1

    df_hbs.loc[(df_hbs['educmom'] == 7) | (df_hbs['educmom'] == 8), 'unimom'] = 1
    df_hbs.loc[(df_hbs['educdad'] == 7) | (df_hbs['educdad'] == 8), 'unidad'] = 1
    
    # immigrant
    df_hbs['immig'] = 0
    df_hbs.loc[(df_hbs['nacmom'] == 2) | (df_hbs['nacmom'] == 3), 'immig'] = 1

    # mom not married
    df_hbs['smom'] = 0
    df_hbs.loc[df_hbs['ecivmom'] != 2, 'smom'] = 1
    
    # siblings
    df_hbs['sib'] = 0
    df_hbs.loc[df_hbs['nmiem2']>1, 'sib'] = 1
    
    # age
    df_hbs['age2'] = df_hbs.agemom * df_hbs.agemom
    df_hbs['age3'] = df_hbs.agemom * df_hbs.agemom * df_hbs.agemom
    
    # daycare
    df_hbs['daycare_bin'] = 0
    df_hbs.loc[df_hbs['m_exp12312']>0 , 'daycare_bin'] = 1
    
    return df_hbs

# preparing df_hbs for further analyses:
    
def preparation_hbs():
    df_hbs = read_and_manipulate_hbs()
    
    # creating interaction terms:
    df_hbs['post_month'] = df_hbs.post * df_hbs.month
    df_hbs['post_month2'] = df_hbs.post * df_hbs.month2

    #creating dummy variables for month of the interview 
    df_hbs.mes_enc = df_hbs.mes_enc.astype(int)
    I_mes_enc = pd.get_dummies(df_hbs['mes_enc'],drop_first=True, prefix='mes_enc')
    df_hbs.drop('mes_enc',axis=1, inplace=True)
    df_hbs = pd.concat([df_hbs,I_mes_enc], axis=1)

    #creating dummy variables for the calender month of birth
    df_hbs.n_month = df_hbs.n_month.astype(int)
    I_n_month = pd.get_dummies(df_hbs['n_month'],drop_first=True, prefix='n_month')
    df_hbs = pd.concat([df_hbs,I_n_month], axis=1)

    # outcome variables in logs:
    df_hbs['ltotexp'] = np.nan
    df_hbs.loc[df_hbs['gastmon']!=0, 'ltotexp'] = np.log(df_hbs.gastmon)
    df_hbs['lcexp'] = np.nan
    df_hbs.loc[df_hbs['c_m_exp']!=0, 'lcexp'] = np.log(df_hbs.c_m_exp)
    df_hbs['ldurexp'] = np.nan
    df_hbs.loc[df_hbs['dur_exp']!=0, 'ldurexp'] = np.log(df_hbs.dur_exp)

    return df_hbs

# printing regression output table for household expenditures:
    
def table_expenditures(dep_vars,dep_vars_name,reg_spec1,reg_spec2,reg_spec3,reg_spec4,reg_spec5,reg_spec6,reg_spec7):
    print('\u2014'*103)
    print('{:<19s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format("", "RDD 9m", \
      "RDD 6m", "RDD 4m", "RDD 3m", "RDD 2m", "RDD 2m", "DiD 1"))
    print('{:<19s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format("", "(1)", \
      "(2)", "(3)", "(4)", "(5)", "(6)", "(7)"))
    print('\u2014'*103)
    x=0
    while x < len(dep_vars):
        print('{:<19s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}'.format(\
          dep_vars_name[x], reg_spec1[x].params.post, reg_spec2[x].params.post, \
          reg_spec3[x].params.post, reg_spec4[x].params.post, reg_spec5[x].params.post, \
          reg_spec6[x].params.post, reg_spec7[x].params.post))
        print('\33[34m' '{:<19s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}' '\33[0m'.format("", \
          reg_spec1[x].bse.post, reg_spec2[x].bse.post, reg_spec3[x].bse.post, \
          reg_spec4[x].bse.post, reg_spec5[x].bse.post, reg_spec6[x].bse.post, \
          reg_spec7[x].bse.post ))
        print('\33[31m' '{:<19s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}' '\33[0m'.format("", \
          reg_spec1[x].pvalues.post, reg_spec2[x].pvalues.post, reg_spec3[x].pvalues.post, \
          reg_spec4[x].pvalues.post, reg_spec5[x].pvalues.post, reg_spec6[x].pvalues.post, \
          reg_spec7[x].pvalues.post ))
        print(""*103)
  
        x += 1
    print('\u2014'*103)
    print("Notes: For each of the dependent variables, the coefficient, standard error and p-value of the binary")
    print("treatment indicator variable are reported:")
    print ('- coefficient estimates')
    print ('\33[34m' '- standard errors' '\33[0m')
    print ('\33[31m' '- p-values' '\33[0m')
    

#printing regression output for childcare:
    
def table_childcare(dep_vars_childcare,dep_vars_childcare_name,reg_spec1_childcare,reg_spec2_childcare,reg_spec3_childcare,reg_spec4_childcare,reg_spec5_childcare,reg_spec6_childcare,reg_spec7_childcare):  
    print('\u2014'*109)
    print('{:<24s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format("", "RDD 9m", \
          "RDD 6m", "RDD 4m", "RDD 3m", "RDD 2m", "RDD 2m", "DiD 1"))
    print('{:<24s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format("", "(1)", \
          "(2)", "(3)", "(4)", "(5)", "(6)", "(7)*"))
    print('\u2014'*109)
    x=0
    while x < len(dep_vars_childcare):
        print('{:<24s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}'.format(\
              dep_vars_childcare_name[x], reg_spec1_childcare[x].params.post, reg_spec2_childcare[x].params.post, \
              reg_spec3_childcare[x].params.post, reg_spec4_childcare[x].params.post, reg_spec5_childcare[x].params.post, \
              reg_spec6_childcare[x].params.post, reg_spec7_childcare[x].params.post))
        print('\33[34m' '{:<24s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}' '\33[0m'.format("", \
              reg_spec1_childcare[x].bse.post, reg_spec2_childcare[x].bse.post, reg_spec3_childcare[x].bse.post, \
              reg_spec4_childcare[x].bse.post, reg_spec5_childcare[x].bse.post, reg_spec6_childcare[x].bse.post, \
              reg_spec7_childcare[x].bse.post ))
        print('\33[31m' '{:<24s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}' '\33[0m'.format("", \
                    reg_spec1_childcare[x].pvalues.post, reg_spec2_childcare[x].pvalues.post, reg_spec3_childcare[x].pvalues.post, \
                    reg_spec4_childcare[x].pvalues.post, reg_spec5_childcare[x].pvalues.post, reg_spec6_childcare[x].pvalues.post, \
                    reg_spec7_childcare[x].pvalues.post ))
        print(""*109)
        x += 1
    print('\u2014'*109)
    print("Notes: For each of the dependent variables, the coefficient, standard error and p-value of the binary")
    print("treatment indicator variable are reported:")
    print ('- coefficient estimates')
    print ('\33[34m' '- standard errors' '\33[0m')
    print ('\33[31m' '- p-values' '\33[0m')



#******************************************************************************
#********************** DATA PROCESSING BASED ON dofile_lfs *******************
#******************************************************************************
    
   
# reading in data set lfs and processing it: 

def read_and_manipulate_lfs():
    
    # read in data:
    df_lfs = pd.read_stata("data/data_lfs_20110196.dta")
    
    # control vars:
    df_lfs['m2']=df_lfs.m * df_lfs.m
    
    # no father present
    df_lfs['nodad'] = 0
    df_lfs.loc[df_lfs['dadid'] == 0, 'nodad'] = 1

    # mother not married

    df_lfs['smom'] = np.nan
    df_lfs.loc[df_lfs['eciv'] == 2, 'smom'] = 0
    df_lfs.loc[(df_lfs['eciv'] == 1) | (df_lfs['eciv'] == 3) | (df_lfs['eciv'] == 4), 'smom'] = 1
    # here, the authors sets smom to 0 for eciv=. in stata

    # mother separated or divorced:
    df_lfs['sepdiv'] = 0
    df_lfs.loc[df_lfs['eciv'] == 4, 'sepdiv'] = 1

    # no partner in the household
    df_lfs['nopart'] = 0
    df_lfs.loc[df_lfs['partner'] == 0, 'nopart'] = 1
    
    # Probability of the mother being in the maternity leave period at the time of the interview
    df_lfs['pleave'] = 0
    values = [0.17,0.5,0.83]
    x = 0
    while x < 3:
        df_lfs.loc[((df_lfs['q']==1) & (df_lfs['m']==2+x)) | ((df_lfs['q']==2) & (df_lfs['m']==5+x)) | \
                   ((df_lfs['q']==3) & (df_lfs['m']==8+x)) | ((df_lfs['q']==4) & (df_lfs['m']==11+x)), \
                   'pleave'] = values[x]
        x += 1
  
    df_lfs.loc[((df_lfs['q']==1) & (df_lfs['m']>4) & (df_lfs['m']<9)) | ((df_lfs['q']==2) & (df_lfs['m']>7) & (df_lfs['m']<12)) | \
               ((df_lfs['q']==3) & (df_lfs['m']>10) & (df_lfs['m']<15)) | ((df_lfs['q']==4) & (df_lfs['m']>13)), \
               'pleave'] = 1

    return df_lfs

# preparing df_lfs for further analyses:
    
def preparation_lfs():
    
    df_lfs = read_and_manipulate_lfs()
   
    # preparation of dummy variables and interaction terms:
    df_lfs.q = df_lfs.q.astype(int)
    I_q = pd.get_dummies(df_lfs['q'],drop_first=True, prefix='q')
    df_lfs = pd.concat([df_lfs,I_q], axis=1)

    df_lfs.n_month = df_lfs.n_month.astype(int)
    I_n_month = pd.get_dummies(df_lfs['n_month'],drop_first=True, prefix='n_month')
    df_lfs = pd.concat([df_lfs,I_n_month], axis=1)

    df_lfs['post_m'] = df_lfs.post * df_lfs.m
    df_lfs['post_m2'] = df_lfs.post * df_lfs.m2
   
    return df_lfs

#printing regression output for labor supply:
    
def table_LS(dep_vars_LS, dep_vars_LS_name, reg_spec1_LS, reg_spec2_LS, reg_spec3_LS, reg_spec4_LS, reg_spec5_LS, reg_spec6_LS, reg_spec7_LS, reg_spec8_LS):
    print('\u2014'*116)
    print('{:<20s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format("", "RDD 9m", \
          "RDD 6m", "RDD 4m", "RDD 3m", "RDD 2m", "RDD 2m", "DiD 1", "DID 1*"))
    print('{:<20s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format("", "(1)", \
          "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)"))
    print('\u2014'*116)
    x=0
    while x < len(dep_vars_LS):
        print('{:<20s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}'.format(\
              dep_vars_LS_name[x], reg_spec1_LS[x].params.post, reg_spec2_LS[x].params.post, \
              reg_spec3_LS[x].params.post, reg_spec4_LS[x].params.post, reg_spec5_LS[x].params.post, \
              reg_spec6_LS[x].params.post, reg_spec7_LS[x].params.post, reg_spec8_LS[x].params.post))
        print('\33[34m' '{:<20s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}' '\33[0m'.format("", \
              reg_spec1_LS[x].bse.post, reg_spec2_LS[x].bse.post, reg_spec3_LS[x].bse.post, \
              reg_spec4_LS[x].bse.post, reg_spec5_LS[x].bse.post, reg_spec6_LS[x].bse.post, \
              reg_spec7_LS[x].bse.post, reg_spec8_LS[x].bse.post ))
        print('\33[31m' '{:<20s}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}{:>12.3f}' '\33[0m'.format("", \
              reg_spec1_LS[x].pvalues.post, reg_spec2_LS[x].pvalues.post, reg_spec3_LS[x].pvalues.post, \
              reg_spec4_LS[x].pvalues.post, reg_spec5_LS[x].pvalues.post, reg_spec6_LS[x].pvalues.post, \
              reg_spec7_LS[x].pvalues.post, reg_spec8_LS[x].pvalues.post ))
        print(""*116)
        x += 1
    print('\u2014'*116)
    print("Notes: For each of the dependent variables, the coefficient, standard error and p-value of the binary")
    print("treatment indicator variable are reported:")
    print ('- coefficient estimates')
    print ('\33[34m' '- standard errors' '\33[0m')
    print ('\33[31m' '- p-values' '\33[0m')




#******************************************************************************
# Appending existing birth data set 
#******************************************************************************

def create_births():
    # read in birth data again
    df_births = pd.read_stata('data/data_births_20110196.dta')
    df_births.year = df_births.year.astype(int)
    df_births.mesp = df_births.mesp.astype(int)
    df_births.prem = df_births.prem.astype(int)
    
    # append data for the years 2011-2017:
    years = ["2011", "2012", "2013", "2014", "2015", "2016", "2017"]

    list_2011_2017 = []
    for year in years:
        path = "data/partos_"+year+".csv"
        df = pd.read_csv(path, sep = ';')
        list_2011_2017.append(df)
         
    x = 0
    while x < 7:
        list_2011_2017[x].year = list_2011_2017[x].year.astype(int)
        list_2011_2017[x].mesp = list_2011_2017[x].mesp.astype(int)
        list_2011_2017[x].prem = list_2011_2017[x].prem.astype(int)
        df_births = df_births.append(list_2011_2017[x], ignore_index = True)
        x += 1
        
    return df_births


#******************************************************************************
#********************** Abolishment of the Policy *****************************
#******************************************************************************
   
# preparing data set for analysis:
    
def preparation_abolishment(df):
    df_births2 = df
    # Create month of birth variable
    df_births2['m'] = np.nan
    
    x = 0
    while x < 18:
        df_births2.loc[df_births2['year'] == 2017 - x, 'm'] = df_births2['mesp'] + 79 - (x*12)
        x += 1
    
    df_births2.loc[df_births2['year']==2010, ['year', 'mesp', 'm']]

    # Create month of conception

    df_births2['mc'] = np.where((df_births2['prem'] == 2) |
        # if premature baby subtract only 8 months to get month of conception
        ((0 < df_births2['semanas']) & (df_births2['semanas'] < 39)), df_births2['m'] - 8,
        # otherwise if baby was born only after 43 months --> -10
        np.where(df_births2['semanas'] > 43, df_births2['m'] - 10,
        # otherwise  - 9
        df_births2['m'] - 9))

    df_births2['n'] = 1
    df_abolishment = df_births2.groupby('mc', as_index = False)['n'].count()
    
    # Create calender month of conception:
    df_abolishment['month'] = 0

    for i in range(9):
        df_abolishment.loc[df_abolishment['mc'] == 0 + 12*i, 'month'] = 5
        df_abolishment.loc[df_abolishment['mc'] == 1 + 12*i, 'month'] = 6
        df_abolishment.loc[df_abolishment['mc'] == 2 + 12*i, 'month'] = 7
        df_abolishment.loc[df_abolishment['mc'] == 3 + 12*i, 'month'] = 8
        df_abolishment.loc[df_abolishment['mc'] == 4 + 12*i, 'month'] = 9
        df_abolishment.loc[df_abolishment['mc'] == 5 + 12*i, 'month'] = 10
        df_abolishment.loc[df_abolishment['mc'] == 6 + 12*i, 'month'] = 11
        df_abolishment.loc[df_abolishment['mc'] == 7 + 12*i, 'month'] = 12
        df_abolishment.loc[df_abolishment['mc'] == 8 + 12*i, 'month'] = 1
        df_abolishment.loc[df_abolishment['mc'] == 9 + 12*i, 'month'] = 2
        df_abolishment.loc[df_abolishment['mc'] == 10 + 12*i, 'month'] = 3
        df_abolishment.loc[df_abolishment['mc'] == 11 + 12*i, 'month'] = 4
        
    for i in range(12):
        df_abolishment.loc[df_abolishment['mc'] == -1 - 12*i, 'month'] = 4
        df_abolishment.loc[df_abolishment['mc'] == -2 - 12*i, 'month'] = 3
        df_abolishment.loc[df_abolishment['mc'] == -3 - 12*i, 'month'] = 2
        df_abolishment.loc[df_abolishment['mc'] == -4 - 12*i, 'month'] = 1
        df_abolishment.loc[df_abolishment['mc'] == -5 - 12*i, 'month'] = 12
        df_abolishment.loc[df_abolishment['mc'] == -6 - 12*i, 'month'] = 11
        df_abolishment.loc[df_abolishment['mc'] == -7 - 12*i, 'month'] = 10
        df_abolishment.loc[df_abolishment['mc'] == -8 - 12*i, 'month'] = 9
        df_abolishment.loc[df_abolishment['mc'] == -9 - 12*i, 'month'] = 8
        df_abolishment.loc[df_abolishment['mc'] == -10 - 12*i, 'month'] = 7
        df_abolishment.loc[df_abolishment['mc'] == -11 - 12*i, 'month'] = 6
        df_abolishment.loc[df_abolishment['mc'] == -12 - 12*i, 'month'] = 5

    # generate May indicator
    df_abolishment['may'] = np.where(df_abolishment['month'] == 5, 1, 0)

    # number of days in a month
    df_abolishment['days'] = np.where((df_abolishment['mc'] == 21) | (df_abolishment['mc'] == 69) |
            (df_abolishment['mc'] == -27) | (df_abolishment['mc'] == -75) | (df_abolishment['mc'] == -123), 29,
            # for all other feburarys
            np.where(df_abolishment['month'] == 2, 28,
            # for April, June, September, November
            np.where((df_abolishment['month'] == 4) | (df_abolishment['month'] == 6) |
            (df_abolishment['month'] == 9) | (df_abolishment['month'] == 11), 30, 31)))

    # indicator for treatment group (post-policy conception), i.e. after June 2007
    df_abolishment['post'] = np.where(df_abolishment['mc'] >= 0, 1, 0)

    # quadratic and cubic mc:
    df_abolishment['mc2'] = df_abolishment['mc']*df_abolishment['mc']
    df_abolishment['mc3'] = df_abolishment['mc']*df_abolishment['mc']*df_abolishment['mc']

    # natural log of number of obs n
    df_abolishment['ln'] = np.log(df_abolishment['n'])

    # get month dummies
    dummies = pd.get_dummies(df_abolishment['month'])
    dummies.columns = ['jan','feb','mar','apr','mai','jun','jul','aug','sep','oct','nov','dec']
    # bind data frames
    df_abolishment = pd.concat([df_abolishment, dummies], axis=1)
   
    return df_abolishment

# regression output table for the abolishment of the policy:
    
def table_abolishment(reg_list_abolishment):
    print('\u2014'*72)
    print('{:<12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'
          .format("", "RDD (1)", "RDD (2)", "RDD (3)", "RDD (4)", "DID (5)"))
    print('{:<12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'
          .format("", "5 years", "12 months", "9 months", "3 months", "5 years"))
    print('\u2014'*72)
    print('{:<12s}'.format("Conceptions"), end="")
    for i in range(len(reg_list_abolishment)):
        print ('{:>12.4f}'.format(reg_list_abolishment[i].params.post), end="")
    print(" "*72)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_list_abolishment)):
        print ('\33[34m' '{:>12.4f}' '\33[0m'.format(reg_list_abolishment[j].bse.post), end="")
    print(" "*72)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_list_abolishment)):
        print ('\33[31m' '{:>12.4f}' '\33[0m'.format(reg_list_abolishment[j].pvalues.post), end="")
    
    print(" "*72)
    print('\u2014'*72)
    print("Notes: The dependent variable is the natural logarithm of the monthly number of conceptions.")
    print("For each of the specifications, the coefficient, standard error and p-value of the binary treatment indicator")
    print("variable are reported:")
    print ('- coefficient estimates')
    print ('\33[34m' '- standard errors' '\33[0m')
    print ('\33[31m' '- p-values' '\33[0m')
    
   
