from objects.environment import Environment
from objects.environment_generator import Environment_Generator
from globals import Globals
from objects.doctor_bot import DoctorBot
from objects.morgue_bot import MorgueBot
from objects.scavenger_bot import ScavengerBot



bots = [ScavengerBot([1, 1], 0), ScavengerBot([7, 1], 1), ScavengerBot([17, 1], 2), ScavengerBot([25, 1], 3),
            DoctorBot([1, 1], 4), DoctorBot([1, 1], 5), DoctorBot([1, 1], 6),
            MorgueBot([1, 1], 7), MorgueBot([1, 1], 8), MorgueBot([1, 1], 9)]
# bots = [DoctorBot([1, 1], 0), DoctorBot([8.5, 10], 1), DoctorBot([2, 1], 2)]

        # [DoctorBot([1, 1], 4), MorgueBot([1, 1], 5)]

globals = Globals()
environment = Environment(globals, bots)

environment.run_sim()
