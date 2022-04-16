from objects.environment import Environment
from objects.environment_generator import Environment_Generator
from globals import Globals
from objects.doctor_bot import DoctorBot
from objects.morgue_bot import MorgueBot
from objects.scavenger_bot import ScavengerBot



bots = [MorgueBot([8.5, 10], 1), DoctorBot([2, 1], 2), ScavengerBot([1, 1], 3),
        DoctorBot([1, 1], 4), MorgueBot([1, 1], 5)]

globals = Globals()
environment = Environment(globals, bots)

environment.run_sim()
