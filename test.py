from objects.environment import Environment
from objects.environment_generator import Environment_Generator
from globals import Globals
from objects.bot import Bot




bots = [Bot([1, 1]), Bot([1, 1]), Bot([1, 1])]

globals = Globals()
environment = Environment(globals, bots)

environment.run_sim()
