# Student project by Antonia Entorf & Marc Lipfert

</a> 
<a href="https://mybinder.org/v2/gh/HumanCapitalAnalysis/student-project-antonia-marc/master?filepath=student_project_Antonia_Marc.ipynb" 
     target="_parent">
     <img align="center" 
        src="https://mybinder.org/badge_logo.svg" 
        width="109" height="20">
</a>

Our project aims at replicating the main results of the following article:

González , L. (2013): The Effect of a Universal Child Benefit on Conceptions, Abortions, and Early Maternal Labor Supply. American Economic Journal: Economic Policy 5(3): 160–188. [(link to the paper)](https://www.aeaweb.org/articles?id=10.1257/pol.5.3.160)


[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/student-project-antonia-marc/master?filepath=student_project_Antonia-Marc.ipynb)


Done:
- replicating main results
- applying the research design to the abolishment of the policy and studying the effect on conceptions
- replicating main plots
- small improvements/corrections compared to the author's data analysis:
  - calculating month of conception with more accuracy (this will affect about 2% of observations)
  - correct minor mistakes in generating calendar month of birth variable
  - correct number of days in a month by accounting for leap years (for some reason the author only took one leap year into account)
- placebo test


To Do:
- there should be a heterogenous treatment effect among rather rich and poor families --> we aim at estimating two different effects to       gain more precise information about the treatment effect
- examine whether accounting for autocorrelation is necessary in the given context
- we might investigate threats to validity using simulations


[//]: <> (Comment: Badges for Travis CI, MIT License and Black Code Style)

[![Build Status](https://travis-ci.org/HumanCapitalAnalysis/student-project-timmens.svg?branch=master)](https://travis-ci.org/HumanCapitalAnalysis/student-project-antonia-marc) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](HumanCapitalAnalysis/student-project-antonia-marc/blob/master/LICENSE)
