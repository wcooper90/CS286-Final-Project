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

        # generate landscape
        self.env = Environment_Generator(globals)
        self.casualties = self.env.casualties
        self.obstacles = self.env.obstacles

        # global parameters
        self.time = globals.time
        self.globals = globals

        # collection of vertex nodes
        self.graph_object = Graph(self.casualties, self.obstacles, self.bots)


    # driver function
    def run_sim(self):

        # keep track of bot locations over time for plotting
        x = []
        y = []
        for i, bot in enumerate(self.bots):
            x.append([bot.location[0]])
            y.append([bot.location[1]])

        # iterate through predetermined amount of time
        for i in range(self.time):
            for bot in self.bots:

                # if a bot has no casualty assigned to it, assign one
                # if there are obstacles, use dijkstra's to calculate a trajectory
                if not bot.finished:
                    if bot.casualty_number is None:
                        self.assign_casualty(bot)
                    if self.obstacles and not bot.next_point and bot.casualty_number is not None:
                        self.plan_bot_trajectory(bot)

                # update a bot's input
                self.update_bot_input(bot)

            # update the system state each iteration
            self.update()

            # only append every third data point from each bot
            if i % 3 == 0:
                for j, bot in enumerate(self.bots):
                    x[j].append(bot.location[0])
                    y[j].append(bot.location[1])

            # create a plot every 10 iterations
            if i % 10 == 0:
                self.save_plot(x, y, i)
                print("Iteration: " + str(i))
                # self.env_check()


    # TODO, a checking function run after every iteration to make sure constraints
    # have not been violated
    def env_check(self):
        if self.obstacles:
            for bot in self.bots:
                position = [bot.location[0], bot.location[1]]
                assert(self.env.container_checker(position))


    # plan a bot's trajectory using Dijkstra's algorithm from the Graph class
    def plan_bot_trajectory(self, bot):
        bot.next_point = self.graph_object.dijkstras(bot.location, [self.casualties[bot.casualty_number][0], self.casualties[bot.casualty_number][1]])


    # update a particular bot's input
    def update_bot_input(self, bot):

        # if a bot has a target to reach,
        if bot.casualty_number is not None:

            casualty = self.env.casualties[bot.casualty_number]

            # if the bot is within a specified distance from the casualty, consider the casualty reached
            if math.dist(bot.location, [casualty[0], casualty[1]]) < self.globals.min_dist_from_casualty:
                # start the aiding timer
                bot.aiding_timer += 1
                bot.input = [0, 0]
                bot.aiding = True
                # switch the actual location of the bot to the original location of the casualty
                bot.location = [casualty[0], casualty[1]]

            # if the bot is within a specified distance from its trajectory's next point, switch to the next point as a target
            elif self.obstacles and math.dist(bot.location, [bot.next_point[0][0], bot.next_point[0][1]]) < self.globals.min_dist_from_casualty:
                bot.location = [bot.next_point[0][0], bot.next_point[0][1]]
                bot.next_point.pop(0)

            # if the bot is not currently aiding a casualty
            if bot.aiding_timer == 0:
                # define the vector the bot needs to progress in the direction of
                if self.obstacles:
                    casualty_vec = np.array([[bot.next_point[0][0]], [bot.next_point[0][1]]])
                else:
                    casualty_vec = np.array([[casualty[0]], [casualty[1]]])

                # find the normalized difference of the bot's vector and its target's vector to find bot input
                bot_vec = np.array([[bot.location[0]], [bot.location[1]]])
                diff_vec = casualty_vec - bot_vec
                directional_norm = list(diff_vec / np.sqrt(np.sum(diff_vec**2)))
                bot.input = [directional_norm[0][0], directional_norm[1][0]]

            # if the bot has already been at a casualty for 5 time steps, reset everything
            # and change the casualty's icon to mark it as aided
            elif bot.aiding_timer >= 5:
                self.env.casualties[bot.casualty_number][2] = 'v'
                bot.aiding_timer = 0
                bot.casualty_number = None
                bot.aiding = False
                bot.next_point = None
            else:
                bot.aiding_timer += 1

        # if the bot does not have a target, keep it still
        else:
            bot.input = [0, 0]


    # assign the nearest casualty for a given bot in Euclidean distance
    def assign_casualty(self, bot):

        # hard coded ceiling
        casualty_number = None
        min_dist = 1000
        # find closest casualty
        for i, casualty in enumerate(self.env.casualties):
            if not casualty[3]:
                point = (casualty[0], casualty[1])
                dist = math.dist(bot.location, point)
                if dist < min_dist:
                    min_dist = dist
                    casualty_number = i

        # if a number is found, mark the casualty so no other bots go towards it
        if casualty_number is not None:
            bot.aiding = True
            bot.casualty_number = casualty_number
            self.env.casualties[casualty_number][3] = True
        # otherwise, there must be no more casualties left in the system
        else:
            bot.finished = True


    # tell each bot to actually update its position based on its calculated input
    def update(self):
        for bot in self.bots:
            bot.update()


    # save a plot of the bots, casualties, obstacles, and bot trajectories
    def save_plot(self, x, y, title):

        # set up the plot
        fig, ax = plt.subplots()
        points = []

        # plot casualties and attach their number
        plt.axes(ax)
        for i in range(len(self.env.casualties)):
            plt.scatter(self.casualties[i][0], self.casualties[i][1], marker=self.casualties[i][2], color='r')
            plt.text(self.casualties[i][0], self.casualties[i][1], str(i))
        ax.set_aspect('equal', 'datalim')

        # plot obstacles
        for shape in self.obstacles:
            xs, ys = shape.exterior.xy
            ax.fill(xs, ys, alpha=0.7, fc='r', ec='none')

        # plot trajectories, color coded to match bot type
        ax.set_xlim((-1, self.globals.x_max))
        ax.set_ylim((-1, self.globals.y_max))
        for i in range(len(self.bots)):
            plt.scatter(x[i], y[i], color=self.bots[i].color, marker='+')

        # save 
        plt.savefig(os.getcwd() + "/data/" + str(title) + ".png")
