# Economic Dispatch of Thermal Units via Ant Colony Optimization

## Pedro Henrique Peters Barbosa & João Pedro Peters Barbosa 

contact: [pedro.peters@engenharia.ufjf.br](pedro.peters@engenharia.ufjf.br), [joao.peters@engenharia.ufjf.br](joao.peters@engenharia.ufjf.br) 

---

This repo contains the simulation results regarding the implementation of ant colony optimization methodology considering the economic dispatch of thermal units.

The Ant Colony Optimization was implemented in both Python and MATLAB programming languages, in order to validate the simulation results and also compare the computational burdens associated in each approach. The main files present in this repo are in the [python folder](./python/) whereas the validation files are in the [matlab folder.](./matlab/)

An academic version of MATLAB®2018 was used in this project.

In the [python folder](./python/), the main files are:

1) [main.py](./python/main.py)
	- Where the Ant Colony Optimization parameters are defined.

2) [pt1_ACO_CVXOPT.py](./python/pt1_ACO_CVXOPT.py)
	- Employs the CVXOPT library parameters in the optimization problem.

3) [pt2_ACO_SEQ.py](./python/pt2_ACO_SEQ.py)
	- Adjusts the data for the problem.

4) [pt3_ACO_PLOT.py](./python/pt3_ACO_PLOT.py)
	- Graphical illustrations of the simulations held.

> Comment out lines 277, 279 e 280 from main.py to avoid the plotting and saving of figures.

The following libraries are needed for the correct functioning of the simulation:

```sh
cvxopt

imageio

matplotlib

numpy

random

timeit

oct2py

scipy
```

Data from thermoelectric systems used in simulation can be found in both folders, under '.m' and '.mat' saving formats.

---

> " Pouca saúde e muita saúva, os males do Brasil são. " - Macunaíma em *Carta pra Icamiabas*
