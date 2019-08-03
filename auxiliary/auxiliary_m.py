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

# printing regression output table for household expenditures:
    
def table_expenditures(dep_vars,dep_vars_name,reg_spec1,reg_spec2,reg_spec3,reg_spec4,reg_spec5,reg_spec6,reg_spec7):
    
    print('\u2014'*103)
    print('{:<19s}{:>11s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}'.format("",\
          "RDD 9m", "", "RDD 6m", "", "RDD 4m", "", "RDD 3m", "", "RDD 2m", "", "RDD 2m", "", "MFE", ""))
    print('{:<19s}{:>11s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}'.format("", \
          "(1)", "", "(2)", "", "(3)", "", "(4)", "", "(5)", "", "(6)", "", "(7)", ""))
    print('\u2014'*103)
    x=0
    while x < len(dep_vars):
        print( '{:<19s}' '\033[1m' '{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}' '\033[0m'.format(dep_vars_name[x], \
          reg_spec1[x].params.post, star_function(reg_spec1[x].pvalues.post), \
          reg_spec2[x].params.post, star_function(reg_spec2[x].pvalues.post), \
          reg_spec3[x].params.post, star_function(reg_spec3[x].pvalues.post), \
          reg_spec4[x].params.post, star_function(reg_spec4[x].pvalues.post), \
          reg_spec5[x].params.post, star_function(reg_spec5[x].pvalues.post), \
          reg_spec6[x].params.post, star_function(reg_spec6[x].pvalues.post), \
          reg_spec7[x].params.post, star_function(reg_spec7[x].pvalues.post)))
        print('{:<19s}{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}'.format("", \
          reg_spec1[x].bse.post, "", reg_spec2[x].bse.post, "", reg_spec3[x].bse.post, "", \
          reg_spec4[x].bse.post, "", reg_spec5[x].bse.post, "", reg_spec6[x].bse.post, "", \
          reg_spec7[x].bse.post, "" ))
        '''
        print('\33[31m' '{:<19s}{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}' '\33[0m'.format("", \
          reg_spec1[x].pvalues.post, "", reg_spec2[x].pvalues.post, "", reg_spec3[x].pvalues.post, "", \
          reg_spec4[x].pvalues.post, "", reg_spec5[x].pvalues.post, "", reg_spec6[x].pvalues.post, "", \
          reg_spec7[x].pvalues.post, ""))
        '''
        print(""*103)
  
        x += 1
    print('{:<19s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Linear trend in m", "Yes", "Yes", "Yes", "No", "No", "No", "Yes"))
    print('{:<19s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Quad. trend in m", "Yes", "No", "No", "No", "No", "No", "Yes"))
    print('{:<19s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Controls", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes"))
    print('\u2014'*103)
    print("Notes: For each of the dependent variables, the coefficient of the binary treatment indicator variable")
    print("is printed in bold font. Heteroscedasticity-robust standard errors are always reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')
    

#printing regression output for childcare:
    
def table_childcare(dep_vars_childcare,dep_vars_childcare_name,reg_spec1_childcare,reg_spec2_childcare,reg_spec3_childcare,reg_spec4_childcare,reg_spec5_childcare,reg_spec6_childcare,reg_spec7_childcare):  
    print('\u2014'*109)
    print('{:<24s}{:>11s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}'.format("", \
          "RDD 9m", "","RDD 6m", "", "RDD 4m", "", "RDD 3m", "", "RDD 2m", "", "RDD 2m", "", "MFE", ""))
    print('{:<24s}{:>11s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}'.format("", \
          "(1)", "", "(2)", "", "(3)", "", "(4)", "", "(5)", "", "(6)", "", "(7)", ""))
    print('\u2014'*109)
    x=0
    while x < len(dep_vars_childcare):
        print('{:<24s}' '\033[1m' '{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}' '\033[0m'.format(dep_vars_childcare_name[x], \
              reg_spec1_childcare[x].params.post, star_function(reg_spec1_childcare[x].pvalues.post), \
              reg_spec2_childcare[x].params.post, star_function(reg_spec2_childcare[x].pvalues.post), \
              reg_spec3_childcare[x].params.post, star_function(reg_spec3_childcare[x].pvalues.post), \
              reg_spec4_childcare[x].params.post, star_function(reg_spec4_childcare[x].pvalues.post), \
              reg_spec5_childcare[x].params.post, star_function(reg_spec5_childcare[x].pvalues.post), \
              reg_spec6_childcare[x].params.post, star_function(reg_spec6_childcare[x].pvalues.post), \
              reg_spec7_childcare[x].params.post, star_function(reg_spec7_childcare[x].pvalues.post) ))
        print('{:<24s}{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}'.format("", \
              reg_spec1_childcare[x].bse.post, "", reg_spec2_childcare[x].bse.post, "", reg_spec3_childcare[x].bse.post, "", \
              reg_spec4_childcare[x].bse.post, "", reg_spec5_childcare[x].bse.post, "", reg_spec6_childcare[x].bse.post, "", \
              reg_spec7_childcare[x].bse.post, "" ))
        '''
        print('\33[31m' '{:<24s}{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}' '\33[0m'.format("", \
                    reg_spec1_childcare[x].pvalues.post, "", reg_spec2_childcare[x].pvalues.post, "", reg_spec3_childcare[x].pvalues.post, "", \
                    reg_spec4_childcare[x].pvalues.post, "", reg_spec5_childcare[x].pvalues.post, "", reg_spec6_childcare[x].pvalues.post, "",\
                    reg_spec7_childcare[x].pvalues.post, "" ))
        '''
        print(""*109)
        x += 1
    print('{:<24s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Linear trend in m", "Yes", "Yes", "Yes", "No", "No", "No", "Yes"))
    print('{:<24s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Quad. trend in m", "Yes", "No", "No", "No", "No", "No", "Yes"))
    print('{:<24s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Controls", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes"))
    print('\u2014'*109)
    print("Notes: For each of the dependent variables, the coefficient of the binary treatment indicator variable is")
    print("printed in bold font. The corresponding heteroscedasticity-robust standard errors are always reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')



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
    
def table_LS(dep_vars_LS, dep_vars_LS_name, reg_spec1_LS, reg_spec2_LS, reg_spec3_LS, reg_spec4_LS, reg_spec5_LS, reg_spec6_LS, reg_spec7_LS):
    print('\u2014'*104)
    print('{:<18s}{:>11s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}'.format("", \
          "RDD 9m", "", "RDD 6m", "", "RDD 4m", "", "RDD 3m", "", "RDD 2m", "", "RDD 2m", "", "MFE", ""))
    print('{:<18s}{:>11s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}{:>9s}{:<3s}'.format("", \
          "(1)", "", "(2)", "", "(3)", "", "(4)", "", "(5)", "", "(6)", "", "(7)", ""))
    print('\u2014'*104)
    x=0
    while x < len(dep_vars_LS):
        print('{:<18s}' '\033[1m' '{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}' '\033[0m'.format(dep_vars_LS_name[x], \
              reg_spec1_LS[x].params.post, star_function( reg_spec1_LS[x].pvalues.post), \
              reg_spec2_LS[x].params.post, star_function( reg_spec2_LS[x].pvalues.post), \
              reg_spec3_LS[x].params.post, star_function( reg_spec3_LS[x].pvalues.post), \
              reg_spec4_LS[x].params.post, star_function( reg_spec4_LS[x].pvalues.post), \
              reg_spec5_LS[x].params.post, star_function( reg_spec5_LS[x].pvalues.post), \
              reg_spec6_LS[x].params.post, star_function( reg_spec6_LS[x].pvalues.post), \
              reg_spec7_LS[x].params.post, star_function( reg_spec7_LS[x].pvalues.post) ))
        print('{:<18s}{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}'.format("", \
              reg_spec1_LS[x].bse.post, "", reg_spec2_LS[x].bse.post, "", reg_spec3_LS[x].bse.post, "", \
              reg_spec4_LS[x].bse.post, "", reg_spec5_LS[x].bse.post, "", reg_spec6_LS[x].bse.post, "", \
              reg_spec7_LS[x].bse.post, ""))
        '''
        print('\33[31m' '{:<18s}{:>12.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}{:>9.3f}{:<3s}' '\33[0m'.format("", \
              reg_spec1_LS[x].pvalues.post, "", reg_spec2_LS[x].pvalues.post, "", reg_spec3_LS[x].pvalues.post, "", \
              reg_spec4_LS[x].pvalues.post, "", reg_spec5_LS[x].pvalues.post, "", reg_spec6_LS[x].pvalues.post, "", \
              reg_spec7_LS[x].pvalues.post, "",  reg_spec8_LS[x].pvalues.post, "" ))
        '''
        print(""*104)
        x += 1
    print('{:<18s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Linear trend in m", "Yes", "Yes", "Yes", "No", "No", "No", "Yes"))
    print('{:<18s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Quad. trend in m", "Yes", "No", "No", "No", "No", "No", "Yes"))
    print('{:<18s}{:>11s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}'.format(\
          "Controls", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes"))
    print('\u2014'*104)
    print("Notes: For each of the dependent variables, the coefficient of the binary treatment indicator variable")
    print("is printed in bold font. For all specifications, standard errors are heteroscedasticity-robust.")
    print("Additionally, standard errors are clustered at the monthly level in the MFE specification.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')




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
    df_births2['mc'] = np.nan
    
    # compute month of conception using information about #-of weeks of pregancy (semanas)
    df_births2.loc[(0 < df_births2['semanas']) & (df_births2['semanas'] <= 21), 'mc'] = df_births2['m'] - 4
    df_births2.loc[(21 < df_births2['semanas']) & (df_births2['semanas'] <= 25), 'mc'] = df_births2['m'] - 5
    df_births2.loc[(25 < df_births2['semanas']) & (df_births2['semanas'] <= 29), 'mc'] = df_births2['m'] - 6
    df_births2.loc[(29 < df_births2['semanas']) & (df_births2['semanas'] <= 34), 'mc'] = df_births2['m'] - 7
    df_births2.loc[(34 < df_births2['semanas']) & (df_births2['semanas'] <= 38), 'mc'] = df_births2['m'] - 8
    df_births2.loc[(38 < df_births2['semanas']) & (df_births2['semanas'] <= 43), 'mc'] = df_births2['m'] - 9
    df_births2.loc[43 < df_births2['semanas'], 'mc'] = df_births2['m'] - 10
    
    # if semanas is missing: approximate mc using premature baby indicator (like the author)
    df_births2.loc[(np.isnan(df_births2['semanas']) | (0 == df_births2['semanas'])) & (df_births2['prem'] == 1), 'mc'] = df_births2['m'] - 9
    df_births2.loc[(np.isnan(df_births2['semanas']) | (0 == df_births2['semanas'])) & (df_births2['prem'] == 2), 'mc'] = df_births2['m'] - 8


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
    print('\u2014'*94)
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}{:>12s}{:<3s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", \
          "RDD (1)", "", "RDD (2)", "", "RDD (3)", "", "RDD (4)", "", "MFE (5)", ""))
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}{:>12s}{:<3s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", \
          "5 years", "", "12 months", "", "9 months", "", "3 months", "", "5 years", ""))
    print('\u2014'*94)
    print('{:<18s}'.format("Conceptions"), end="")
    for i in range(len(reg_list_abolishment)):
        print ('\033[1m' '{:>12.4f}{:<3s}' '\033[0m'.format(reg_list_abolishment[i].params.post, star_function(reg_list_abolishment[i].pvalues.post)), end="")
    print(" "*87)
    print('{:<18s}'.format(""), end="")
    for j in range(len(reg_list_abolishment)):
        print ( '{:>12.4f}{:<3s}'.format(reg_list_abolishment[j].bse.post,""), end="")
    '''
    print(" "*87)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_list_abolishment)):
        print ('\33[31m' '{:>12.4f}{:<3s}' '\33[0m'.format(reg_list_abolishment[j].pvalues.post, ""), end="")
    '''
    print(" "*87)
    print(" "*87)
    print('{:<18s}{:>12s}{:>15s}{:>15s}{:>15s}{:>15s}'.format(\
          "Linear trend in m", "Yes", "Yes", "Yes", "No", "Yes"))
    print('{:<18s}{:>12s}{:>15s}{:>15s}{:>15s}{:>15s}'.format(\
          "Quad. trend in m", "Yes", "Yes", "No", "No", "Yes"))
    print('\u2014'*94)
    print("Notes: The dependent variable is the natural logarithm of the monthly number of conceptions.")
    print("For each of the specifications, the coefficient of the binary treatment indicator variable is")
    print("printed in bold font. The corresponding standard errors are always reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')
    
   
#******************************************************************************
#********************** Placebo Tests *****************************************
#******************************************************************************

###############################################################################
# July as Threshold
    
# preparing data set:
def preparation_placebo_july(df):
    df_births3 = df
    
    # Create month of birth variable
    df_births3['m'] = np.nan

    x = 0
    while x < 18:
        df_births3.loc[df_births3['year'] == 2017 - x, 'm'] = df_births3['mesp'] + 5 - (x*12)
        x += 1
    
    df_births3.loc[df_births3['year']==2016, ['year', 'mesp', 'm']]

    # Create month of conception
    df_births3['mc'] = np.nan
    
        # compute month of conception using information about #-of weeks of pregancy (semanas)
    df_births3.loc[(0 < df_births3['semanas']) & (df_births3['semanas'] <= 21), 'mc'] = df_births3['m'] - 4
    df_births3.loc[(21 < df_births3['semanas']) & (df_births3['semanas'] <= 25), 'mc'] = df_births3['m'] - 5
    df_births3.loc[(25 < df_births3['semanas']) & (df_births3['semanas'] <= 29), 'mc'] = df_births3['m'] - 6
    df_births3.loc[(29 < df_births3['semanas']) & (df_births3['semanas'] <= 34), 'mc'] = df_births3['m'] - 7
    df_births3.loc[(34 < df_births3['semanas']) & (df_births3['semanas'] <= 38), 'mc'] = df_births3['m'] - 8
    df_births3.loc[(38 < df_births3['semanas']) & (df_births3['semanas'] <= 43), 'mc'] = df_births3['m'] - 9
    df_births3.loc[43 < df_births3['semanas'], 'mc'] = df_births3['m'] - 10
    
    # if semanas is missing: approximate mc using premature baby indicator (like the author)
    df_births3.loc[(np.isnan(df_births3['semanas']) | (0 == df_births3['semanas'])) & (df_births3['prem'] == 1), 'mc'] = df_births3['m'] - 9
    df_births3.loc[(np.isnan(df_births3['semanas']) | (0 == df_births3['semanas'])) & (df_births3['prem'] == 2), 'mc'] = df_births3['m'] - 8
 
    df_births3['n'] = 1
    df_placebo_july = df_births3.groupby('mc', as_index = False)['n'].count()
    
    # Create calender month of conception:

    df_placebo_july['month'] = 0

    for i in range(3):
        df_placebo_july.loc[df_placebo_july['mc'] == 0 + 12*i, 'month'] = 7
        df_placebo_july.loc[df_placebo_july['mc'] == 1 + 12*i, 'month'] = 8
        df_placebo_july.loc[df_placebo_july['mc'] == 2 + 12*i, 'month'] = 9
        df_placebo_july.loc[df_placebo_july['mc'] == 3 + 12*i, 'month'] = 10
        df_placebo_july.loc[df_placebo_july['mc'] == 4 + 12*i, 'month'] = 11
        df_placebo_july.loc[df_placebo_july['mc'] == 5 + 12*i, 'month'] = 12
        df_placebo_july.loc[df_placebo_july['mc'] == 6 + 12*i, 'month'] = 1
        df_placebo_july.loc[df_placebo_july['mc'] == 7 + 12*i, 'month'] = 2
        df_placebo_july.loc[df_placebo_july['mc'] == 8 + 12*i, 'month'] = 3
        df_placebo_july.loc[df_placebo_july['mc'] == 9 + 12*i, 'month'] = 4
        df_placebo_july.loc[df_placebo_july['mc'] == 10 + 12*i, 'month'] = 5
        df_placebo_july.loc[df_placebo_july['mc'] == 11 + 12*i, 'month'] = 6
       
    for i in range(18):
        df_placebo_july.loc[df_placebo_july['mc'] == -1 - 12*i, 'month'] = 6
        df_placebo_july.loc[df_placebo_july['mc'] == -2 - 12*i, 'month'] = 5
        df_placebo_july.loc[df_placebo_july['mc'] == -3 - 12*i, 'month'] = 4
        df_placebo_july.loc[df_placebo_july['mc'] == -4 - 12*i, 'month'] = 3
        df_placebo_july.loc[df_placebo_july['mc'] == -5 - 12*i, 'month'] = 2
        df_placebo_july.loc[df_placebo_july['mc'] == -6 - 12*i, 'month'] = 1
        df_placebo_july.loc[df_placebo_july['mc'] == -7 - 12*i, 'month'] = 12
        df_placebo_july.loc[df_placebo_july['mc'] == -8 - 12*i, 'month'] = 11
        df_placebo_july.loc[df_placebo_july['mc'] == -9 - 12*i, 'month'] = 10
        df_placebo_july.loc[df_placebo_july['mc'] == -10 - 12*i, 'month'] = 9
        df_placebo_july.loc[df_placebo_july['mc'] == -11 - 12*i, 'month'] = 8
        df_placebo_july.loc[df_placebo_july['mc'] == -12 - 12*i, 'month'] = 7

    # generate July indicator
    df_placebo_july['july'] = np.where(df_placebo_july['month'] == 7, 1, 0)

    # number of days in a month
    df_placebo_july['days'] = np.where((df_placebo_july['mc'] == -5) | (df_placebo_july['mc'] == -53) |
        (df_placebo_july['mc'] == -101) | (df_placebo_july['mc'] == -149) | (df_placebo_july['mc'] == -197), 29,
        # for all other feburarys
        np.where(df_placebo_july['month'] == 2, 28,
        # for April, June, September, November
        np.where((df_placebo_july['month'] == 4) | (df_placebo_july['month'] == 6) |
                (df_placebo_july['month'] == 9) | (df_placebo_july['month'] == 11), 30, 31)))

    # indicator for placebo treatment group (post-policy)
    df_placebo_july['post'] = np.where(df_placebo_july['mc'] >= 0, 1, 0)

    # quadratic and cubic mc:
    df_placebo_july['mc2'] = df_placebo_july['mc']*df_placebo_july['mc']
    df_placebo_july['mc3'] = df_placebo_july['mc']*df_placebo_july['mc']*df_placebo_july['mc']

    
    # natural log of number of obs n
    df_placebo_july['ln'] = np.log(df_placebo_july['n']) 
    
    return df_placebo_july

# regression output table for placebo test July:
def table_placebo_july(reg_list_placebo_july):
    
    print('\u2014'*47)
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", "RDD (1)", "", "RDD (2)", ""))
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", "9 months", "", "3 months", ""))
    print('\u2014'*47)
    print('{:<18s}'.format("Conceptions"), end="")
    for i in range(len(reg_list_placebo_july)):
        print ('\033[1m' '{:>12.4f}{:<3s}' '\033[0m'.format(reg_list_placebo_july[i].params.post,\
                                                            star_function(reg_list_placebo_july[i].pvalues.post)), end="")
    print(" "*40)
    print('{:<18s}'.format(""), end="")
    for j in range(len(reg_list_placebo_july)):
        print ('{:>12.4f}{:<3s}'.format(reg_list_placebo_july[j].bse.post, ""), end="")
    '''
    print(" "*40)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_list_placebo_july)):
        print ('\33[31m' '{:>12.4f}{:<3s}' '\x1b[0m'.format(reg_list_placebo_july[j].pvalues.post, ""), end="")
    '''
    print(" "*40)
    print(" "*40)
    print('{:<18s}{:>12s}{:>15s}'.format(\
          "Linear trend in m", "Yes", "No"))
    
    print('\u2014'*47)  
    print("Notes: The dependent variable is the natural logarithm of the monthly number of conceptions.")
    print("For each of the specifications, the coefficient of the binary treatment indicator is printed")
    print("in bold font. Heteroscedasticity-robust standard errors are reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')
    
    
##############################################################################
# May as threshold
    
# prepartion of the data set:
    
def preparation_placebo_may(df):
    df_births4 = df
    
    # Create month of birth variable
    df_births4['m'] = np.nan

    x = 0
    while x < 18:
        df_births4.loc[df_births4['year'] == 2017 - x, 'm'] = df_births4['mesp'] + 7 - (x*12)
        x += 1
    
    df_births4.loc[df_births4['year']==2016, ['year', 'mesp', 'm']]

    # Create month of conception
    df_births4['mc'] = np.nan
    
        # compute month of conception using information about #-of weeks of pregancy (semanas)
    df_births4.loc[(0 < df_births4['semanas']) & (df_births4['semanas'] <= 21), 'mc'] = df_births4['m'] - 4
    df_births4.loc[(21 < df_births4['semanas']) & (df_births4['semanas'] <= 25), 'mc'] = df_births4['m'] - 5
    df_births4.loc[(25 < df_births4['semanas']) & (df_births4['semanas'] <= 29), 'mc'] = df_births4['m'] - 6
    df_births4.loc[(29 < df_births4['semanas']) & (df_births4['semanas'] <= 34), 'mc'] = df_births4['m'] - 7
    df_births4.loc[(34 < df_births4['semanas']) & (df_births4['semanas'] <= 38), 'mc'] = df_births4['m'] - 8
    df_births4.loc[(38 < df_births4['semanas']) & (df_births4['semanas'] <= 43), 'mc'] = df_births4['m'] - 9
    df_births4.loc[43 < df_births4['semanas'], 'mc'] = df_births4['m'] - 10
    
    # if semanas is missing: approximate mc using premature baby indicator (like the author)
    df_births4.loc[(np.isnan(df_births4['semanas']) | (0 == df_births4['semanas'])) & (df_births4['prem'] == 1), 'mc'] = df_births4['m'] - 9
    df_births4.loc[(np.isnan(df_births4['semanas']) | (0 == df_births4['semanas'])) & (df_births4['prem'] == 2), 'mc'] = df_births4['m'] - 8

    df_births4['n'] = 1
    df_placebo_may = df_births4.groupby('mc', as_index = False)['n'].count()
    
    # Create calender month of conception:

    df_placebo_may['month'] = 0

    for i in range(3):
        df_placebo_may.loc[df_placebo_may['mc'] == 0 + 12*i, 'month'] = 5
        df_placebo_may.loc[df_placebo_may['mc'] == 1 + 12*i, 'month'] = 6
        df_placebo_may.loc[df_placebo_may['mc'] == 2 + 12*i, 'month'] = 7
        df_placebo_may.loc[df_placebo_may['mc'] == 3 + 12*i, 'month'] = 8
        df_placebo_may.loc[df_placebo_may['mc'] == 4 + 12*i, 'month'] = 9
        df_placebo_may.loc[df_placebo_may['mc'] == 5 + 12*i, 'month'] = 10
        df_placebo_may.loc[df_placebo_may['mc'] == 6 + 12*i, 'month'] = 11
        df_placebo_may.loc[df_placebo_may['mc'] == 7 + 12*i, 'month'] = 12
        df_placebo_may.loc[df_placebo_may['mc'] == 8 + 12*i, 'month'] = 1
        df_placebo_may.loc[df_placebo_may['mc'] == 9 + 12*i, 'month'] = 2
        df_placebo_may.loc[df_placebo_may['mc'] == 10 + 12*i, 'month'] = 3
        df_placebo_may.loc[df_placebo_may['mc'] == 11 + 12*i, 'month'] = 4
       
    for i in range(18):
        df_placebo_may.loc[df_placebo_may['mc'] == -1 - 12*i, 'month'] = 4
        df_placebo_may.loc[df_placebo_may['mc'] == -2 - 12*i, 'month'] = 3
        df_placebo_may.loc[df_placebo_may['mc'] == -3 - 12*i, 'month'] = 2
        df_placebo_may.loc[df_placebo_may['mc'] == -4 - 12*i, 'month'] = 1
        df_placebo_may.loc[df_placebo_may['mc'] == -5 - 12*i, 'month'] = 12
        df_placebo_may.loc[df_placebo_may['mc'] == -6 - 12*i, 'month'] = 11
        df_placebo_may.loc[df_placebo_may['mc'] == -7 - 12*i, 'month'] = 10
        df_placebo_may.loc[df_placebo_may['mc'] == -8 - 12*i, 'month'] = 9
        df_placebo_may.loc[df_placebo_may['mc'] == -9 - 12*i, 'month'] = 8
        df_placebo_may.loc[df_placebo_may['mc'] == -10 - 12*i, 'month'] = 7
        df_placebo_may.loc[df_placebo_may['mc'] == -11 - 12*i, 'month'] = 6
        df_placebo_may.loc[df_placebo_may['mc'] == -12 - 12*i, 'month'] = 5

    # generate May indicator
    df_placebo_may['may'] = np.where(df_placebo_may['month'] == 5, 1, 0)



    # number of days in a month
    df_placebo_may['days'] = np.where((df_placebo_may['mc'] == -3) | (df_placebo_may['mc'] == -51) |
        (df_placebo_may['mc'] == -99) | (df_placebo_may['mc'] == -147) | (df_placebo_may['mc'] == -195), 29,
        # for all other feburarys
        np.where(df_placebo_may['month'] == 2, 28,
        # for April, June, September, November
        np.where((df_placebo_may['month'] == 4) | (df_placebo_may['month'] == 6) |
                (df_placebo_may['month'] == 9) | (df_placebo_may['month'] == 11), 30, 31)))


    # indicator for treatment group (post-policy conception), i.e. after June 2007
    df_placebo_may['post'] = np.where(df_placebo_may['mc'] >= 0, 1, 0)

    # quadratic and cubic mc:
    df_placebo_may['mc2'] = df_placebo_may['mc']*df_placebo_may['mc']
    df_placebo_may['mc3'] = df_placebo_may['mc']*df_placebo_may['mc']*df_placebo_may['mc']

    df_placebo_may[['mc','mc2','mc3']].head()

    # natural log of number of obs n
    df_placebo_may['ln'] = np.log(df_placebo_may['n']) 
    
    return df_placebo_may

    
# regression output table for placebo test May:
  
def table_placebo_may(reg_list_p2):

    print('\u2014'*49)
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", "RDD (1)", "", "RDD (2)", ""))
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", "9 months", "", "3 months", ""))
    print('\u2014'*49)
    print('{:<18s}'.format("Conceptions"), end="")
    for i in range(len(reg_list_p2)):
        print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_list_p2[i].params.post,\
                                                           star_function(reg_list_p2[i].pvalues.post)), end="")
    print(" "*43)
    print('{:<18s}'.format(""), end="")
    for j in range(len(reg_list_p2)):
        print ('{:>12.4f}{:<3s}'.format(reg_list_p2[j].bse.post, ""), end="")
    '''
    print(" "*43)
    print('{:<12s}'.format(""), end="")
    for j in range(len(reg_list_p2)):
        print ('\33[31m' '{:>12.4f}{:<3s}' '\x1b[0m'.format(reg_list_p2[j].pvalues.post, ""), end="")
    '''
    print(" "*43)
    print(" "*40)
    print('{:<18s}{:>12s}{:>15s}'.format(\
          "Linear trend in m", "Yes", "No"))
    print('\u2014'*49)  
    print("Notes: The dependent variable is the natural logarithm of the monthly number of conceptions.")
    print("For each of the specifications, the coefficient of the binary treatment indicator is printed")
    print("in bold font. Heteroscedasticity-robust standard errors are reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')
    
    
    
#******************************************************************************
#********************** Autocorrelation ***************************************
#******************************************************************************

# Newey-West regressions for conceptions

def reg_conceptions_NW(data_frame):
    
    # create necessary subsets of data_frame
    dfb_list = list()
    dfb_list.append(data_frame.loc[(data_frame['mc']>-91) & (data_frame['mc']<30)]) # 10 years
    dfb_list.append(data_frame.loc[(data_frame['mc']>-67) & (data_frame['mc']<30)]) # 8 years
    
    # Newey West regressions:
    reg6_NW = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + mc3 + post*mc3 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfb_list[0]).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    reg7_NW = smf.ols(formula =
            'ln ~ post + mc + post*mc + mc2 + post*mc2 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfb_list[1]).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    
    # store regression results in list
    reg_list_b_NW = [reg6_NW, reg7_NW]

       
    return reg_list_b_NW
    

    
# comparing Results for Conceptions:

def table_conceptions_NW(reg_list_b, reg_list_b_NW):

    print('\u2014'*49)
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", "MFE (6)", "", "MFE (7)", ""))
    print('{:<18s}{:>12s}{:<3s}{:>12s}{:<3s}'.format("", "10 years", "", "7 years", ""))
    print('\u2014'*49)
    print('{:<18s}'.format("Conceptions -"), end="")
    for i in range(5,7):
        print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_list_b[i].params.post,\
                                                           star_function(reg_list_b[i].pvalues.post)), end="")
    print(" "*49)
    print('{:<18s}'.format("  robust SE"), end="")
    for j in range(5,7):
        print ('{:>12.4f}{:<3s}'.format(reg_list_b[j].bse.post, ""), end="")
    
    print(" "*49)
    print(" "*49)
    print('{:<18s}'.format("Conceptions -"), end="")
    for i in range(len(reg_list_b_NW)):
        print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_list_b_NW[i].params.post,\
                                                           star_function(reg_list_b_NW[i].pvalues.post)), end="")
    print(" "*49)
    print('{:<18s}'.format("  Newey West SE"), end="")
    for j in range(len(reg_list_b_NW)):
        print ('{:>12.4f}{:<3s}'.format(reg_list_b_NW[j].bse.post, ""), end="")
    
    print(" "*49)
    print('\u2014'*49)  
    print("Notes: The dependent variable is the natural logarithm of the monthly number of conceptions.")
    print("For each of the specifications, the coefficient of the binary treatment indicator is printed")
    print("in bold font. Standard errors are reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')
   


# Newey-West regressions for abortions

def reg_abortions_NW(data_frame):
    
    # create necessary subsets of data_frame
    dfa_list = list()
    dfa_list.append(data_frame.loc[(data_frame['m']>-31) & (data_frame['m']<30)]) # 5 years
    
    # Newey West regressions:
    reg8_NW = smf.ols(formula =
            'log_ive ~ post + m + post*m + m2 + post*m2 + days + feb + mar + apr + mai + jun + jul + aug + sep + oct + nov + dec', data=dfa_list[0]).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    
    # store regression results in list
    reg_list_a_NW = [reg8_NW]

       
    return reg_list_a_NW 

# comparing Results for abortions:

def table_abortions_NW(reg_list_a, reg_list_a_NW):

    print('\u2014'*40)
    print('{:<18s}{:>12s}{:<3s}'.format("", "MFE (8)", ""))
    print('{:<18s}{:>12s}{:<3s}'.format("", "5 years", ""))
    print('\u2014'*40)
    print('{:<18s}'.format("Abortions -"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_list_a[7].params.post,\
                                                       star_function(reg_list_a[7].pvalues.post)), end="")
    print(" "*49)
    print('{:<18s}'.format("  robust SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_list_a[7].bse.post, ""), end="")
    
    print(" "*49)
    print(" "*49)
    print('{:<18s}'.format("Abortions -"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_list_a_NW[0].params.post,\
                                                       star_function(reg_list_a_NW[0].pvalues.post)), end="")
    print(" "*49)
    print('{:<18s}'.format("  Newey West SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_list_a_NW[0].bse.post, ""), end="")
    
    print(" "*49)
    print('\u2014'*40)  
    print("Notes: The dependent variable is the natural logarithm of the monthly number of abortions.")
    print("The coefficient of the binary treatment indicator is printed in bold font. ")
    print("Standard errors are reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')
    
# comparing Results for labor supply:

def table_LS_ac(reg_spec7_LS_robust, reg_spec7_LS, reg_spec7_LS_NW):

    print('\u2014'*40)
    print('{:<25s}{:>12s}{:<3s}'.format("", "MFE", ""))
    print('{:<25s}{:>12s}{:<3s}'.format("", "(7)", ""))
    print('\u2014'*40)
    print('{:<25s}'.format("Working last week -"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_spec7_LS[0].params.post,""))
    print('{:<25s}'.format("  robust SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_LS_robust[0].bse.post, star_function(reg_spec7_LS_robust[0].pvalues.post)))
    print('{:<25s}'.format("  clustered SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_LS[0].bse.post, star_function(reg_spec7_LS[0].pvalues.post)))
    print('{:<25s}'.format("  Newey-West SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_LS_NW[0].bse.post, star_function(reg_spec7_LS_NW[0].pvalues.post)))
    print(" "*49)

    print('{:<25s}'.format("Employed -"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_spec7_LS[1].params.post,""))
    print('{:<25s}'.format("  robust SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_LS_robust[1].bse.post, star_function(reg_spec7_LS_robust[1].pvalues.post)))
    print('{:<25s}'.format("  clustered SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_LS[1].bse.post, star_function(reg_spec7_LS[1].pvalues.post)))
    print('{:<25s}'.format("  Newey-West SE"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_LS_NW[1].bse.post, star_function(reg_spec7_LS_NW[1].pvalues.post)))
    
    print('\u2014'*40)  
    print("Notes: The coefficient of the binary treatment indicator is always printed in bold font. ")
    print("Standard errors are reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')

 

#******************************************************************************
#********************** Global vs. Local Polynomial ***************************
#******************************************************************************

# comparing Results for daycare:


def table_daycare_poly(reg_spec7_childcare_global, reg_spec7_childcare):

    print('\u2014'*40)
    print('{:<25s}{:>12s}{:<3s}'.format("", "MFE", ""))
    print('{:<25s}{:>12s}{:<3s}'.format("", "(7)", ""))
    print('\u2014'*40)
    print('{:<25s}'.format("Private day care"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_spec7_childcare[0].params.post,\
                                                       star_function(reg_spec7_childcare[0].pvalues.post)))
    print('{:<25s}'.format("- local polynomial"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_childcare[0].bse.post,""))
    print(" "*49)
    
    print('{:<25s}'.format("Private day care"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_spec7_childcare_global[0].params.post,\
                                                       star_function(reg_spec7_childcare_global[0].pvalues.post)))
    print('{:<25s}'.format("- global polynomial"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_childcare_global[0].bse.post,""))
    print(" "*49)

    print('{:<25s}'.format("Priv. day care (binary)"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_spec7_childcare[1].params.post,\
                                                      star_function(reg_spec7_childcare[1].pvalues.post)))
    print('{:<25s}'.format("- local polynomial"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_childcare[1].bse.post, ""))
    print(" "*49)

    print('{:<25s}'.format("Priv. day care (binary)"), end="")
    print ('\033[1m' '{:>12.4f}{:<3s}''\033[0m'.format(reg_spec7_childcare_global[1].params.post,\
                                                      star_function(reg_spec7_childcare_global[1].pvalues.post)))
    print('{:<25s}'.format("- global polynomial"), end="")
    print ('{:>12.4f}{:<3s}'.format(reg_spec7_childcare_global[1].bse.post, ""))
    
    print('\u2014'*40)  
    print("Notes: The coefficient of the binary treatment indicator is always printed in bold font. ")
    print("Heteroscedasticity-robust standard errors are reported below.")
    print ('***Significance at the 1 percent level.')
    print (' **Significance at the 5 percent level.')
    print ('  *Significance at the 10 percent level.')

