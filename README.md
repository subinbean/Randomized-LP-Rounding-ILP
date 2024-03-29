# Randomized-LP-Rounding-ILP
## Overview
### Motivation
- Linear Programming (LP) as well as Integer Linear Programming (ILP) is an extremely valuable abstraction / method for us in tackling NP-hard problems in practice
- When we went from LPs to ILPs in class, we encountered some bad theory news that we can construct IPs whose rounded LP solutions are arbitrarily far away
- However, for some NP-hard problems, we are able to use randomization to round the ILP solution in a clever way so that we can bound our “approximation ratio” (the ratio between the solution we get and the optimal solution.” This is known as the **Randomized LP Rounding Paradigm**

### Project idea
We observed that this setting is a classic example of a runtime versus accuracy tradeoff.
- We are using CP-SAT to solve the ILP version of the problem, which **exactly** solves the problem in **exponential time**
- We are using the GLOP Linear Program Solver to solve the LP version of the problem, and we are implementing a randomized rounding scheme to solve the problem **approximately** in **polynomial time**
- We compare these two approaches for two famous NP-hard Problems: Weighted Set-Cover and Max-SAT)

### LP Rounding Paradigm Refresher
The Randomized LP Rounding Paradigm takes the following approach to approximately solve an NP-hard Problem “K”:
1. Cast K into an Integer Linear Program
2. Drop the Integrality constraints to turn the problem into an LP instance
3. Solve the LP instance of the problem 
4. Use randomization to cleverly round the LP solution into an integer solution
5. Output the rounded solution


## Set Cover
### Results
Everything for the SetCover algorithm implementation is included in `set_cover.py`, and the results are included in `set_cover.ipynb`. For a brief summary here, the randomized rounding scheme we use is including each set with probability p where p is the value assigned to the set by the Liner program. We iterate that procedure log n times where n is the number of elements, and then we for each uncovered element after the log n procedures the minimum weight set that covers it. This approxmation scheme gives us a O(log n) approximation to the problem. We notice from our results that the randomized scheme does extermely well in some cases, but quickly falls off in others. As such, the rounding scheme may be more useful in some cases, but the ILP version gives a very consistent performance (the margin between the optimal value and the ILP value that was cut-off was the same). As such, a mix of the two would be recommended. 

### Dataset Sources
The datasets used for the set cover problem belong to the OR-Library open-sourced by J E Beasley, Professor of Operational Research in the Department of Mathematical Sciences, Brunel University, West London. 

His website can be found here: http://people.brunel.ac.uk/~mastjjb/jeb/jeb.html

And the OR-Library for Set Cover that contains links to the datset can be found here: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html

## MaxSAT
### Data
For MaxSAT, we went with randomly generated data since it gives us the most control over 
the sizes and shapes of the formulae, allowing us to see detailed runtime correlation with 
number of variables and number of clauses. It also allows us to sample over a wide range of
sizes/shapes.

### Results
Everything for MaxSAT is included in `max_sat.ipynb`. Each section is documented, and the current saved version has all the plots, results, and conclusions.
For a brief summary here, we essentially concluded that (1) LP rounding gets really good approximation error in practice, and (2) ILP does really well even when constraining it to 
linear runtime (despite it actually requiring exponential time for optimality).
