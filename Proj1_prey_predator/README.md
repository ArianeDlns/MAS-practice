# Prey - Predator Model

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![Open in Visual Studio Code](https://img.shields.io/badge/Editor-VSCode-blue?style=flat-square&logo=visual-studio-code&logoColor=white)](https://github.dev/ArianeDlns/MAS-practice/tree/master/Proj1_prey_predator)

<p align="center">
<img src="prey_predator/old/resources/wolf.png" alt="wolf" width="200"/> <img src="prey_predator/old/resources/sheep.png" alt="wolf" width="200"/>


## Summary

A simple ecological model, consisting of three agent types: wolves, sheep, and grass. The wolves and the sheep wander around the grid at random. Wolves and sheep both expend energy moving around, and replenish it by eating. Sheep eat grass, and wolves eat sheep if they end up on the same grid cell.

If wolves and sheep have enough energy, they reproduce, creating a new wolf or sheep (in this simplified model, only one parent is needed for reproduction). The grass on each cell regrows at a constant rate. If any wolves and sheep run out of energy, they die.

The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (wolves, sheep, grass)
 - Overlay arbitrary text (wolf's energy) on agent's shapes while drawing on CanvasGrid
 - Agents inheriting a behavior (random movement) from an abstract parent
 - Writing a model composed of multiple files.
 - Dynamically adding and removing agents from the schedule

## Topic of the project

To evaluate the knowledge acquired in this course on Multi-Agent Based Simulations, we suggest you model the Wolf Sheep Predation model which is a variation of the prey predator model. The description of the ABM is as follows:
- Wolves and sheep wander randomly around the landscape, while the wolves look for sheep to prey on.
- Each step costs energy. Wolves must eat sheep in order to replenish their energy. Sheep must eat grass in order to maintain their energy. When sheep and wolves run out of energy they die.
- To allow the population to continue, each wolf or sheep has a fixed probability of reproducing at each time step.
- Grass is also explicitly modeled. Once grass is eaten it will only regrow after a fixed amount of time.

### To Do: 
- [x] 1. Implement the described Wolf Sheep Predation ABM.
- [x] 2. Create a visualization interface to setup and run the simulation.
- [ ] 3. Write a short description of your implementation choices as well as a description of the behavior of the system and how you find the right parameters so that it is stable.
- [ ] 4. Create a zip archive containing the files and upload it on the EDUNAO platform.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## :package: Files

* ``prey_predator/random_walker.py``: This defines the ``RandomWalker`` agent, which implements the behavior of moving randomly across a grid, one cell at a time. Both the Wolf and Sheep agents will inherit from it.
* ``prey_predator/agents.py``: Defines the Wolf, Sheep, and GrassPatch agent classes.
* ``prey_predator/schedule.py``: Defines a custom variant on the RandomActivation scheduler, where all agents of one class are activated (in random order) before the next class goes -- e.g. all the wolves go, then all the sheep, then all the grass.
* ``prey_predator/model.py``: Defines the Prey-Predator model itself
* ``prey_predator/server.py``: Sets up the interactive visualization server
* ``run.py``: Launches a model visualization server.

```
.
├── README.md
├── prey_predator
│   ├── __init__.py
│   ├── agents.py
│   ├── icons
│   │   ├── sheep_icon.png
│   │   └── wolf_icon.png
│   ├── model.py
│   ├── old #Model from mesa example
│   │   ├── agents.py
│   │   ├── model.py
│   │   ├── random_walk.py
│   │   ├── resources
│   │   │   ├── favicon.ico
│   │   │   ├── sheep.png
│   │   │   ├── sheep_old.png
│   │   │   ├── wolf.png
│   │   │   └── wolf_old.png
│   ├── random_walk.py
│   ├── schedule.py
│   └── server.py
├── requirements.txt
├── run.py
└── testing_model.ipynb # Test on notebook
```

## What we did  

- ``prey_predator/server.py``: Sets up the interactive visualization server  
We configured: 
    - wolf_sheep_portrayal
    - model_params
    - MyTextElement
- ``prey_predator/agents.py``: Defines the Wolf, Sheep, and GrassPatch agent classes.  
We configured: 
    - Wolf
    - Sheep
    - Grass 
- ``prey_predator/model.py``: Defines the Prey-Predator model itself  
We configured: 
    - creation of Sheeps
    - creation of Wolves
    - creation of Grass
    - running one step
    - running the whole model

## References

This model is closely based on the NetLogo Wolf-Sheep Predation Model:

Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

See also the [Lotka–Volterra equations
](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) for an example of a classic differential-equation model with similar dynamics.
[Lotka-Volterra](https://strimas.com/post/lotka-volterra/)

Kazil, Jacqueline & Masad, David & Crooks, Andrew. (2020). [Utilizing Python for Agent-Based Modeling: The Mesa Framework.](https://www.researchgate.net/publication/344675633_Utilizing_Python_for_Agent-Based_Modeling_The_Mesa_Framework) 10.1007/978-3-030-61255-9_30. 

The implementation is based on the mesa example that we can find in this [repository](https://github.com/projectmesa/mesa/tree/main/examples/wolf_sheep)