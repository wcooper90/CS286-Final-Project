import matplotlib as plt
from shapely.geometry import Polygon, Point, box
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt
import random
import os


class Environment_Generator():
    def __init__(self, params):
        self.params = params
        self.obstacles = []
        self.generate_obstacles()
        self.casualties = []
        self.generate_casualties()
        self.plot_grid()


    # generator random locations for casualties based on global parameter
    def generate_casualties(self):
        for i in range(self.params.num_casualties):
            point = (round(random.random() * self.params.x_max, 1), round(random.random() * self.params.y_max, 1))
            while not self.casualty_checker(point):
                point = (round(random.random() * self.params.x_max, 1), round(random.random() * self.params.y_max, 1))
            self.casualties.append((point[0], point[1], 'p'))


    # make sure generated casualty point is not in an obstacle
    def casualty_checker(self, point):
        point = Point(point[0], point[1])
        for obstacle in self.obstacles:
            if obstacle.contains(point):
                return False
        return True


    # generate random unit squares as obstacles
    ## TODO: make some of the obstacles triangles
    def generate_obstacles(self):
        for i in range(self.params.num_obstacles):
            init = (random.randint(self.params.x_min, self.params.x_max - 1),
                             random.randint(self.params.y_min, self.params.y_max - 1))

            # to make polygons other than boxes
            # r1 = sg.Polygon([(init[0], init[1]), (init[0], init[1] + 1), (init[0] + 1, init[1]), (init[0] + 1, init[1] + 1)])

            r1 = sg.box(init[0], init[1], init[0] + 1, init[1] + 1)
            self.obstacles.append(r1)


    # plot only the casualties and obstacles
    def plot_grid(self):
        # set up the plot
        fig, ax = plt.subplots()
        points = []

        plt.axes(ax)
        for i in range(len(self.casualties)):
            plt.scatter(self.casualties[i][0], self.casualties[i][1], marker=self.casualties[i][2], color='r')

        ax.set_aspect('equal', 'datalim')

        for shape in self.obstacles:
            xs, ys = shape.exterior.xy
            ax.fill(xs, ys, alpha=0.5, fc='r', ec='none')

        ax.set_xlim((-1, 11))
        ax.set_ylim((-1, 11))

        plt.savefig("initial_grid.png")


    # TODO: create moving obstacles
    def shift_obstacles(self):
        pass 
