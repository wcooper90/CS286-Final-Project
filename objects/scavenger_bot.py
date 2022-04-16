from .bot import Bot
from .enum import BotType


class ScavengerBot(Bot):
    def __init__(self, location, id):
        super().__init__(location)
        self.bot_type = BotType.scavenger
        self.bot_id = id
        self.color = 'y'

    def say_bot_type(self):
        print("My bot_id is " + str(self.bot_id) + " and I am a scavenger bot!")
        return self.bot_type
