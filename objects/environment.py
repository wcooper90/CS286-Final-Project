from .bot import Bot
from .environment_generator import Environment_Generator
from shapely.geometry import Point
from .graph import Graph
import numpy as np
import math
import matplotlib.pyplot as plt
import os


class Environment():
    def __init__(self, globals, bots):

        self.width = globals.width
        self.height = globals.height
        self.res = globals.res
        self.bots = bots
        self.env = Environment_Generator(globals)
        self.casualties = self.env.casualties
        self.obstacles = self.env.obstacles
        self.time = globals.time
        self.globals = globals
        self.graph_object = Graph(self.casualties, self.obstacles, self.bots)


    def run_sim(self):
        x = []
        y = []

        for i, bot in enumerate(self.bots):
            x.append([bot.location[0]])
            y.append([bot.location[1]])

        for i in range(self.time):
            for bot in self.bots:
                if not bot.finished:
                    if bot.casualty_number is None:
                        self.assign_casualty(bot)
                    if self.obstacles and not bot.next_point and bot.casualty_number is not None:
                        self.plan_bot_trajectory(bot)

                self.update_bot_input(bot)

            self.update()
            if i % 3 == 0:
                for j, bot in enumerate(self.bots):
                    x[j].append(bot.location[0])
                    y[j].append(bot.location[1])

            if i % 10 == 0:
                self.save_plot(x, y, i)
                print("Iteration: " + str(i))
                for i, bot in enumerate(self.bots):
                    print(i, bot.casualty_number)
                # self.env_check()


    def env_check(self):
        if self.obstacles:
            for bot in self.bots:
                position = [bot.location[0], bot.location[1]]
                assert(self.env.container_checker(position))


    def plan_bot_trajectory(self, bot):
        # if bot.casualty_number:
        bot.next_point = self.graph_object.dijkstras(bot.location, [self.casualties[bot.casualty_number][0], self.casualties[bot.casualty_number][1]])
        # else:
        #     bot.next_point = [bot.location]
        # if not bot.next_point:


        # plan bot trajectory (the next set of points it should visit)


    def update_bot_input(self, bot):
        # if a bot is within a certain distance of the point it was supposed to visit,
        # update to move to next point
        # if the next point is close enough to a casualty, start the casualty timer
        if bot.casualty_number is not None:

            casualty = self.env.casualties[bot.casualty_number]

            if math.dist(bot.location, [casualty[0], casualty[1]]) < self.globals.min_dist_from_casualty:
                bot.aiding_timer += 1
                bot.input = [0, 0]
                bot.aiding = True
                bot.location = [casualty[0], casualty[1]]

            elif self.obstacles and math.dist(bot.location, [bot.next_point[0][0], bot.next_point[0][1]]) < self.globals.min_dist_from_casualty:
                bot.location = [bot.next_point[0][0], bot.next_point[0][1]]
                bot.next_point.pop(0)

            if bot.aiding_timer == 0:
                if self.obstacles:
                    casualty_vec = np.array([[bot.next_point[0][0]], [bot.next_point[0][1]]])
                else:
                    casualty_vec = np.array([[casualty[0]], [casualty[1]]])

                bot_vec = np.array([[bot.location[0]], [bot.location[1]]])
                diff_vec = casualty_vec - bot_vec
                directional_norm = list(diff_vec / np.sqrt(np.sum(diff_vec**2)))
                bot.input = [directional_norm[0][0], directional_norm[1][0]]

            elif bot.aiding_timer >= 10:
                self.env.casualties[bot.casualty_number][2] = 'v'
                bot.aiding_timer = 0
                bot.casualty_number = None
                bot.aiding = False
                bot.next_point = None
            else:
                bot.aiding_timer += 1
        else:
            bot.input = [0, 0]


    def assign_casualty(self, bot):

        # hard coded ceiling
        casualty_number = None
        min_dist = 1000
        for i, casualty in enumerate(self.env.casualties):
            if not casualty[3]:
                point = (casualty[0], casualty[1])
                dist = math.dist(bot.location, point)
                if dist < min_dist:
                    min_dist = dist
                    casualty_number = i

        if casualty_number is not None:
            bot.aiding = True
            bot.casualty_number = casualty_number
            self.env.casualties[casualty_number][3] = True
        else:
            bot.finished = True


    def update(self):
        for bot in self.bots:
            bot.update()


    def save_plot(self, x, y, title):
        # set up the plot
        fig, ax = plt.subplots()
        points = []

        plt.axes(ax)
        for i in range(len(self.env.casualties)):
            plt.scatter(self.casualties[i][0], self.casualties[i][1], marker=self.casualties[i][2], color='r')
            plt.text(self.casualties[i][0], self.casualties[i][1], str(i))

        ax.set_aspect('equal', 'datalim')

        for shape in self.obstacles:
            xs, ys = shape.exterior.xy
            ax.fill(xs, ys, alpha=0.5, fc='r', ec='none')

        ax.set_xlim((-1, 11))
        ax.set_ylim((-1, 11))

        for i in range(len(self.bots)):
            plt.scatter(x[i], y[i], marker='+')

        plt.savefig(os.getcwd() + "/data/" + str(title) + ".png")
