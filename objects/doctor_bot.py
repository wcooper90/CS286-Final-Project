from .bot import Bot
from .enum import BotType, CasualtyType


class DoctorBot(Bot):
    def __init__(self, location, id):
        super().__init__(location)
        self.bot_type = BotType.doctor
        self.bot_id = id
        self.color = 'g'
        self.assigned_casualty_type = CasualtyType.injured

    def say_bot_type(self):
        print("My bot_id is " + str(self.bot_id) + " and I am a doctor bot!")
        return self.bot_type
