/***************************************************************************/
/**************		ENCUESTA DE PRESUPUESTOS FAMILIARES 2008   *************/
/***************************************************************************/

/* Here I run the regression analysis reported in Tables 4 and 6.*/

clear all
clear matrix
set mem 500m

use data_hbs_20110196, clear

/***** 1. Control variables. *****/
/* Characteristics: age of mom and dad, education of mom and dad, mom foreing, mom not married, mom or dad not present.*/
sum agemom agedad educmom educdad nacmom ecivmom

/* Age of mom and dad.*/
replace agemom=0 if agemom==.
replace agedad=0 if agedad==.

/* Mom or dad not present.*/
drop nomom nodad
gen nomom=0
gen nodad=0
replace nomom=1 if agemom==0
replace nodad=1 if agedad==0
sum nomom nodad

/* Education of mom and dad.*/
gen sec1mom=0
gen sec1dad=0
gen sec2mom=0
gen sec2dad=0
gen unimom=0
gen unidad=0

replace sec1mom=1 if educmom==3
replace sec1dad=1 if educdad==3

replace sec2mom=1 if educmom>3 & educmom<7
replace sec2dad=1 if educdad>3 & educdad<7

replace unimom=1 if educmom==7 | educmom==8
replace unidad=1 if educdad==7 | educdad==8

sum sec1mom sec1dad sec2mom sec2dad unimom unidad

/* Immigrant.*/
/* (Dummy for mom with foreing nationality.)*/
gen immig=0
replace immig=1 if nacmom==2 | nacmom==3

sum immig

/* Mom not married.*/
gen smom=0
replace smom=1 if ecivmom!=2

sum agemom agedad nomom nodad sec1mom sec1dad sec2mom sec2dad unimom unidad immig smom

/* Siblings.*/
gen sib=0
replace sib=1 if nmiem2>1

gen age2=agemom*agemom
gen age3=agemom*agemom*agemom

gen daycare_bin=0
replace daycare_bin=1 if m_exp12312>0 & m_exp12312!=.

sum gastmon c_m_exp dur_exp m_exp12312 post month agemom sec1mom sec2mom unimom immig sib if month>-10 & month<9
centile gastmon c_m_exp dur_exp m_exp12312 post month agemom sec1mom sec2mom unimom immig sib if month>-10 & month<9

/**************************		TABLE 4. MAIN EXPENDITURE RESULTS	******************************************************************************/

/*************************** 			Total expenditure.		*************************************************/
xi:reg gastmon post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg gastmon post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg gastmon post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg gastmon post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg gastmon post if month>-3 & month<2, robust
xi:reg gastmon post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg gastmon post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc i.n_month, robust

/****************************		 	Child-related expenditure.		*****************************************/
xi:reg c_m_exp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg c_m_exp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg c_m_exp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg c_m_exp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg c_m_exp post if month>-3 & month<2, robust
xi:reg c_m_exp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg c_m_exp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc i.n_month, robust

/****************************		 	Durable goods expenditure.		*****************************************/
xi:reg dur_exp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg dur_exp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg dur_exp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg dur_exp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg dur_exp post if month>-3 & month<2, robust
xi:reg dur_exp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg dur_exp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc i.n_month, robust

/*** In logs ***/
gen ltotexp=ln(gastmon)
gen lcexp=ln(c_m_exp)
gen ldurexp=ln(dur_exp)

/*************************** 			Total expenditure.		*************************************************/
xi:reg ltotexp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg ltotexp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg ltotexp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg ltotexp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg ltotexp post if month>-3 & month<2, robust
xi:reg ltotexp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg ltotexp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc i.n_month, robust

/****************************		 	Child-related expenditure.		*****************************************/
xi:reg lcexp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg lcexp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg lcexp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg lcexp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg lcexp post if month>-3 & month<2, robust
xi:reg lcexp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg lcexp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc i.n_month, robust

/****************************		 	Durable goods expenditure.		*****************************************/
xi:reg ldurexp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg ldurexp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg ldurexp post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg ldurexp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg ldurexp post if month>-3 & month<2, robust
xi:reg ldurexp post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg ldurexp post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc i.n_month, robust


/**************************		TABLE 6. CHILDCARE RESULTS	******************************************************************************/

/* Private childcare */
xi:reg m_exp12312 post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg m_exp12312 post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg m_exp12312 post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg m_exp12312 post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg m_exp12312 post if month>-3 & month<2, robust
xi:reg m_exp12312 post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg m_exp12312 post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc i.n_month, robust

xi:reg daycare_bin post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.post|month2 i.mes_enc if month>-10 & month<9, robust
xi:reg daycare_bin post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-7 & month<6, robust
xi:reg daycare_bin post month nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.post|month i.mes_enc if month>-5 & month<4, robust
xi:reg daycare_bin post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-4 & month<3, robust
xi:reg daycare_bin post if month>-3 & month<2, robust
xi:reg daycare_bin post nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc if month>-3 & month<2, robust
xi:reg daycare_bin post month month2 nomom agemom age2 age3 sec1mom sec2mom unimom immig sib i.mes_enc i.n_month, robust
