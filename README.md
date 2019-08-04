# Student project by Antonia Entorf & Marc Lipfert

</a> 
<a href="https://mybinder.org/v2/gh/HumanCapitalAnalysis/student-project-antonia-marc/master?filepath=student_project_Antonia_Marc.ipynb" 
     target="_parent">
     <img align="center" 
        src="https://mybinder.org/badge_logo.svg" 
        width="109" height="20">
</a>
</a>
<a href="https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/student-project-antonia-marc/blob/master/student_project_Antonia_Marc.ipynb"
   target="_parent">
   <img align="center" 
  src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png" 
      width="109" height="20">
</a>

## Replication
This project replicates the main results presented in the following article:   

González, L. (2013): [The Effect of a Universal Child Benefit on Conceptions, Abortions, and Early Maternal Labor Supply](https://www.aeaweb.org/articles?id=10.1257/pol.5.3.160). American Economic Journal: Economic Policy 5(3): 160–188.

In that article, the author investigates the effects of a universal child benefit on fertility, household expenditure patterns and maternal labor supply. In particular, she exploits the unanticipated introduction of such a policy that took place in Spain in 2007 by utilizing a sharp Regression Discontinuity Design.

The author's results suggest a significant increase in fertility, partly driven by a reduction in the number of abortions. Furthermore, she finds no effect on overall household expenditures, a significantly negative effect on mothers' labor supply the year after giving birth and significantly lower use of formal day care.

## Critical Assessment
Apart from replicating key findings, we conduct a critical assessment of the author's empircal work. For this, we examine, first, whether accounting for autocorrelation is necessary in the given context of a regression discontinuity design in time. Secondly, we show revised estimates based on a more precise computation of the month of conception. Thirdly, we examine the impact on the obtained estimates when using a local vs. a global polynomial time trend.

## Further Analyses
Since the benefit was suspended in the aftermath of the financial crisis, we will exploit this fact and apply the identical research design to the abolishment of the policy in order to study the effect on conceptions. Furthermore, we will investigate the general reliability of the research design by executing two Placebo tests and a simulation study of a time-varying treatment effect.


[//]: <> (Comment: Badges for Travis CI, MIT License and Black Code Style)

[![Build Status](https://travis-ci.org/HumanCapitalAnalysis/student-project-antonia-marc.svg?branch=master)](https://travis-ci.org/HumanCapitalAnalysis/student-project-antonia-marc) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](HumanCapitalAnalysis/student-project-antonia-marc/blob/master/LICENSE)
