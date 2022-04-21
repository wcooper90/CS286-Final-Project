from .enum import CasualtyType


class Casualty():
    def __init__(self, location, type, found=False, color='k'):
        self.x = location[0]
        self.y = location[1]
        self.type = type
        self.color = color

        self.found = found
        self.marker = 'p'
        self.assigned = False
