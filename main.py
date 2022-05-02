from objects.environment import Environment
from objects.environment_generator import Environment_Generator
from globals import Globals
from objects.doctor_bot import DoctorBot
from objects.morgue_bot import MorgueBot
from objects.scavenger_bot import ScavengerBot
from objects.enum import PlanningAlgorithmType


# define a set of scavenger, morgue, and doctor bots. Envrionment generator will automatically
# generator obstacles and casualties accordingly
# bots = [ScavengerBot([1, 1], 0), ScavengerBot([7, 1], 1), ScavengerBot([17, 1], 2), ScavengerBot([25, 1], 3),
#             DoctorBot([1, 1], 4), DoctorBot([1, 1], 5), DoctorBot([1, 1], 6),
#             MorgueBot([1, 1], 7), MorgueBot([1, 1], 8), MorgueBot([1, 1], 9)]

# define a simple set of only doctor bots
# bots are defined with DoctorBot([location tuple], unique_id)
bots = [DoctorBot([1, 1], 0), DoctorBot([1, 1], 1), DoctorBot([1, 1], 2)]


# reference the globals.py file to make changes
globals = Globals()
# generate environment
environment = Environment(globals, bots)

# run simulation
environment.run_sim()

# reset the system while keeping the same set of generated obstacles and casualties
environment.reset_system()
# redefine a global variable and rerun the simulation to compare results
environment.globals.planning_algorithm = PlanningAlgorithmType.Global_Dijkstra
environment.run_sim()
