from .enum import CasualtyType


class Casualty():
    def __init__(self, location, type):
        self.x = location[0]
        self.y = location[1]
        self.type = type
        self.color = 'k'

        self.found = False
        self.marker = 'p'
        self.assigned = False
