
/************	ENCUESTA DE POBLACION ACTIVA 2008	*****************/

/* Here we run the labor supply regressions with EPA 2008 data.*/

clear all

set memory 500000

use data_lfs_20110196, clear

/* 1. Control variables.*/

gen m2 = m*m

/* No father present.*/
gen nodad=0
replace nodad=1 if dadid==0

/* Mother not married */
gen smom=0
replace smom=1 if eciv!=2

/* Mother single.*/
gen single=0
replace single=1 if eciv==1

/* Mother separated or divorced.*/
gen sepdiv=0
replace sepdiv=1 if eciv==4

/* No partner in the household.*/
gen nopart=0
replace nopart=1 if partner==0

/* Probability of the mother being in the maternity leave period at the time of the interview.*/
gen pleave=0
replace pleave=0.17 if (q==1 & m==2) | (q==2 & m==5) | (q==3 & m==8) | (q==4 & m==11)
replace pleave=0.5 if (q==1 & m==3) | (q==2 & m==6) | (q==3 & m==9) | (q==4 & m==12)
replace pleave=0.83 if (q==1 & m==4) | (q==2 & m==7) | (q==3 & m==10) | (q==4 & m==13)
replace pleave=1 if (q==1 & m>4 & m<9) | (q==2 & m>7 & m<12) | (q==3 & m>10 & m<15) | (q==4 & m>13)

/* Table 1 Descriptives  */
sum work work2 post m age primary hsgrad univ immig sib if m>-10 & m<9
centile work work2 post m age primary hsgrad univ immig sib if m>-10 & m<9

/**********************************		 Table 5 Regressions		**************************************************/

/**********************************		 Working last week		*****************************************************/
xi: reg work post i.post|m i.post|m2 age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-10 & m<9, robust 
xi: reg work post i.post|m age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-7 & m<6, robust 
xi: reg work post i.post|m age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-5 & m<4, robust 
xi: reg work post age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-4 & m<3, robust
xi: reg work post if m>-3 & m<2, robust 
xi: reg work post age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-3 & m<2, robust
xi: reg work post m m2 age age2 age3 immig primary hsgrad univ sib pleave i.n_month i.q, robust cluster(m)

/**************************************		 Employed		*********************************************************/
xi: reg work2 post i.post|m i.post|m2 age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-10 & m<9, robust 
xi: reg work2 post i.post|m age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-7 & m<6, robust 
xi: reg work2 post i.post|m age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-5 & m<4, robust 
xi: reg work2 post age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-4 & m<3, robust
xi: reg work2 post if m>-3 & m<2, robust 
xi: reg work2 post age age2 age3 immig primary hsgrad univ sib pleave i.q if m>-3 & m<2, robust
xi: reg work2 post m m2 age age2 age3 immig primary hsgrad univ sib pleave i.n_month i.q, robust cluster(m)
