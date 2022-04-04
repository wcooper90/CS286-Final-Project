from .bot import Bot
from .environment_generator import EnvironmentGenerator


class Environment():
    def __init__(self, globals, bots):

        self.width = globals.width
        self.height = globals.height
        self.res = globals.res
        self.bots = bots
        self.generator = EnvironmentGenerator(globals.casualties, globals.obstacles)
        self.casualties = self.generator.casualties
        self.obstacles = self.generator.obstacles



    def run_sim(self):
        self.update()


    def update(self):
        for bot in self.bots:
            bot.update()
