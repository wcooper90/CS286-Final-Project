import enum


class BotType(enum.Enum):
    # bot type class
    scavenger = 1
    doctor = 2
    morgue = 3


class CasualtyType(enum.Enum):
    dead = 1
    injured = 2
