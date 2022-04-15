import numpy as np


class Bot():

    def __init__(self, location, k=0.05):
        self.location = location
        self.input = [0,0]
        self.casualty_number = None

        # change to argument k later
        self.k = 0.05
        self.next_point = None
        self.aiding_timer = 0
        self.aiding = False
        self.trajectory = [location]


    def update(self):
        self.location[0] += self.k * self.input[0]
        self.location[1] += self.k * self.input[1]
        self.trajectory.append(self.location)
        # print(self.trajectory)
        self.input = np.array([0, 0])
