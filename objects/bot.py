import numpy as np


class Bot():

    def __init__(self, location, k=0.2):
        self.location = location
        self.input = [0,0]

        # bot's casualty parameters 
        self.casualty_number = None
        self.aiding_timer = 0
        self.aiding = False
        self.finished = False

        # movement dampener
        self.k = k

        # next point to travel to, according to Dijkstra's
        self.next_point = None



    # bot's update function, applies the new input to its current location
    def update(self):
        if not self.finished:
            self.location[0] += self.k * self.input[0]
            self.location[1] += self.k * self.input[1]

            # reset input to 0 vector
            self.input = np.array([0, 0])
