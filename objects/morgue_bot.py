from .bot import Bot
from .enum import BotType, CasualtyType


class MorgueBot(Bot):
    def __init__(self, location, id):
        super().__init__(location)
        self.bot_type = BotType.morgue
        self.bot_id = id
        self.color = 'm'
        self.assigned_casualty_type = CasualtyType.dead

    def say_bot_type(self):
        print("My bot_id is " + str(self.bot_id) + " and I am a morgue bot!")
        return self.bot_type
