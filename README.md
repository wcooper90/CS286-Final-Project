# Spring 2022
# CS286: Multi-Agent Systems
# Final Project


Repository description:
- graphics:
  - analysis plotting and animation scripts
- data
  - intermediary storage point for deployment frames
- objects:
  - bot.py
    - base class for all bots
  - casualty.py
    - base class for all casualties
  - doctor_bot.py
    - doctor bot class, inherits from bot class
  - enum.py
    - enumeration class for bot types, casualty types, and algorithm types
  - environment_generator.py
    - generates casualties and obstacle objects
  - environment_generator1.py
    - same class as environment_generator but allows for experimental obstacle movement functions
  - environment.py
    - control class, takes in global parameters, generates an environment with environment_generator, generates a graph with graph.py, and conducts iterative simulation, updating bot trajectories
  - graph_node.py
    - node object of graphs
  - graph.py
    - contains algorithms for generating different types of graphs, and contains the Dijkstra's graph traversal algorithm
  - morgue_bot.py
    - morgue bot class, inherits from bot class
  - scavenger_bot.py
    - scavenger bot class, inherits from bot class
- main.py
  - run simulation from here. An example is commented and set up already.
- test.py
- globals.py
  - all alterable user-specified values, referenced by all files in the repository. Variables are commented.


To get started, read the commented code in main.py!
