/******************************************************************************************/
/**************************		1. CONCEPTIONS ANALYSIS	***********************************/
/******************************************************************************************/

clear all
set memory 550m

/* 0. Access the data set.*/
use data_births_20110196, clear

/* Variables.*/
/*
mesp: Month of birth
year: Year of birth
prem: Prematurity indicator
semanas: Weeks of gestation at birth
*/

/* 1. Create month of birth variable.*/
/* (0 = July 2007, 1 = August 2007, etc).*/ 
gen m = mesp + 29 if year==2010
replace m = mesp + 17 if year==2009
replace m = mesp + 5 if year==2008
replace m = mesp - 7 if year==2007
replace m = mesp - 19 if year==2006
replace m = mesp - 31 if year==2005
replace m = mesp - 43 if year==2004
replace m = mesp - 55 if year==2003
replace m = mesp - 67 if year==2002
replace m = mesp - 79 if year==2001
replace m = mesp - 91 if year==2000

sum m

/* 2. Create month of conception variable.*/

/* 2.1. NaÏve definition. */
/* (9 months before the birth month) */
gen mc1 = m - 9

/* 2.2. Naïve plus prematures. */
/* (9 months before the birth month, 8 if premature) */
gen mc2 = m - 9
replace mc2 = m - 8 if (semanas>0 & semanas<38) | prem==2

/* 2.3. Sophisticated.*/
/* (calculated based on weeks of gestation) */
/* (This is the one used in the paper.)*/
gen mc3 = m - 9
replace mc3 = m - 10 if semanas > 43 & semanas!=.
replace mc3 = m - 8 if (semanas < 39 & semanas!=0) | prem==2

/* 3. Label all variables.*/
label var m "Month of birth (0 = July 2007)"
label var mc3 "Month of conception (0 = July 2007)"
label var mesp "Calendar month of birth"
label var year "Year of birth"

/* 4. Collapse by month of conception.*/
gen n=1

collapse (count) n, by(mc3)
rename mc3 mc
sum

/* 5. Calendar month of conception. */
gen month=1 if mc==-30 | mc==-18 | mc==-6 | mc==6 | mc==18 | mc==30 | mc==-42 | mc==-54 | mc==-66 | mc==-87
replace month=2 if mc==-29 | mc==-17 | mc==-5 | mc==7 | mc==19 | mc==31 | mc==-41 | mc==-53 | mc==-65 | mc==-86 | mc==-98
replace month=3 if mc==-28 | mc==-16 | mc==-4 | mc==8 | mc==20 | mc==32 | mc==-40 | mc==-52 | mc==-64 | mc==-85 | mc==-97
replace month=4 if mc==-27 | mc==-15 | mc==-3 | mc==9 | mc==21 | mc==-39 | mc==-51 | mc==-63 | mc==-75 | mc==-84 | mc==-96
replace month=5 if mc==-26 | mc==-14 | mc==-2 | mc==10 | mc==22 | mc==-38 | mc==-50 | mc==-62 | mc==-74 | mc==-83 | mc==-95
replace month=6 if mc==-25 | mc==-13 | mc==-1 | mc==11 | mc==23 | mc==-37 | mc==-49 | mc==-61 | mc==-73 | mc==-82 | mc==-94
replace month=7 if mc==-24 | mc==-12 | mc==0 | mc==12 | mc==24 | mc==-36 | mc==-48 | mc==-60 | mc==-72 | mc==-81 | mc==-93
replace month=8 if mc==-23 | mc==-11 | mc==1 | mc==13 | mc==25 | mc==-35 | mc==-47 | mc==-59 | mc==-71 | mc==-80 | mc==-92
replace month=9 if mc==-22 | mc==-10 | mc==2 | mc==14 | mc==26 | mc==-34 | mc==-46 | mc==-58 | mc==-70 | mc==-79 | mc==-91
replace month=10 if mc==-21 | mc==-9 | mc==3 | mc==15 | mc==27 | mc==-33 | mc==-45 | mc==-57 | mc==-69 | mc==-78 | mc==-90
replace month=11 if mc==-20 | mc==-8 | mc==4 | mc==16 | mc==28 | mc==-32 | mc==-44 | mc==-56 | mc==-68 | mc==-77 | mc==-89
replace month=12 if mc==-19 | mc==-7 | mc==5 | mc==17 | mc==29 | mc==-31 | mc==-43 | mc==-55 | mc==-67 | mc==-76 | mc==-88

/* 6. July indicator.*/
gen july=n if month==7

/* 7. Number of days in a month.*/
gen days=31
replace days=28 if month==2
replace days=29 if mc==7
replace days=30 if month==4 | month==6 | month==9 | month==11

/* 8. A post indicator for post-policy conception.*/
gen post=0
replace post=1 if mc>=0

gen mc2=mc*mc
gen mc3=mc*mc*mc

/* 9. Natural log.*/
gen ln = ln(n)

sum n ln post mc month if mc>-91 & mc<30

/* 10. Regressions Table 2.*/
xi: reg ln post i.post|mc i.post|mc2 i.post|mc3 days if mc>-91 & mc<30, robust
xi: reg ln post i.post|mc i.post|mc2 days if mc>-31 & mc<30, robust
xi: reg ln post i.post|mc i.post|mc2 days if mc>-13 & mc<12, robust
xi: reg ln post i.post|mc days if mc>-10 & mc<9, robust
xi: reg ln post days if mc>-4 & mc<3, robust
xi: reg ln post i.post|mc i.post|mc2 i.post|mc3 days i.month if mc>-91 & mc<30, robust /* 10 years */
xi: reg ln post i.post|mc i.post|mc2 days i.month if mc>-67 & mc<30, robust /* 8 years */
xi: reg ln post i.post|mc i.post|mc2 days i.month if mc>-31 & mc<30, robust /* 5 years */

/******************************************************************************************/
/**************************		2. ABORTIONS ANALYSIS	***********************************/
/******************************************************************************************/

/* This do-file accesses the data on number of abortions per month by region from 1999 to 2010,
and it analyzes whether there was a discontinuity around June 30, 2007.*/

clear all
set mem 200m

/* 1. Access the data.*/

use data_abortions_20110196, clear

sum

/* 2. Label variables */
label var n_ive_and "Number of abortions per month in Andalucia, 1999-2009"
label var n_ive_val "Number of abortions per month in C. Valenciana, 2000-2010"
label var n_ive_rioja "Number of abortions per month in La Rioja, 2000-2009"
label var n_ive_cat "Number of abortions per month in Cataluña, 2000-2009"
label var n_ive_can "Number of abortions per month in Canarias, 1999-2010"
label var n_ive_mad "Number of abortions per month in Madrid, 1999-2009"
label var n_ive_gal "Number of abortions per month in Galicia, 2000-2009"
label var n_ive_bal "Number of abortions per month in Baleares, 2000-2009"
label var n_ive_pv "Number of abortions per month in Pais Vasco, 2000-2009"
label var n_ive_castlm "Number of abortions per month in Castilla La Mancha, 2000-2010"
label var n_ive_ast "Number of abortions per month in Asturias, 2000-2010"
label var n_ive_arag "Number of abortions per month in Aragon, 2000-2010"

/* 3. Sum abortions across all regions.*/
gen n_tot = n_ive_and + n_ive_val + n_ive_rioja + n_ive_cat + n_ive_can + n_ive_mad + n_ive_gal + n_ive_bal + n_ive_pv + n_ive_castlm + n_ive_ast + n_ive_arag 

/* 4. Create month variable that takes value 0 in July 2007.*/
gen m = _n
replace m = m - 103

label variable m "month of birth, 0 = July 2007"
sum

/* 5. Now I generate a variable indicating number of days in a month.*/
gen days=31
replace days=30 if month==4 | month==6 | month==9 | month==11
replace days=28 if month==2
replace days=29 if month==2 & (year==2000 | year==2004 | year==2008)
sum days

/* 6. Now I generate log-abortions.*/
gen log_ive = ln(n_tot)

/* 7. Squared and cubed terms in m.*/
gen m2=m*m
gen m3=m*m*m

/* 8. Post dummy */
gen post=0
replace post=1 if m>=0

/* 9. Restrict period.*/
drop if m<-90 
drop if m>29

sum n_tot log_ive post m month days

/* 10. Regressions. */
xi: reg log_ive post i.post|m i.post|m2 i.post|m3 days, robust
xi: reg log_ive post i.post|m i.post|m2 days if m>-31, robust
xi: reg log_ive post i.post|m i.post|m2 days if m>-13 & m<12, robust
xi: reg log_ive post i.post|m days if m>-10 & m<9, robust
xi: reg log_ive post days if m>-4 & m<3, robust
xi: reg log_ive post i.post|m i.post|m2 i.post|m3 days i.month, robust /* 10 years */
xi: reg log_ive post i.post|m i.post|m2 days i.month if m>-67, robust /* 8 years */
xi: reg log_ive post i.post|m i.post|m2 days i.month if m>-31, robust /* 5 years */
