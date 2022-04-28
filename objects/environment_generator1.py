import matplotlib as plt
from shapely.geometry import Polygon, Point, box
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.ops as so
import random
import os
from .casualty import Casualty
from .enum import CasualtyType, BotType
import copy


class Environment_Generator():

    def __init__(self, params, bots):
        # init function serves as driver code, generate obstacles, casualties, and plot the initial grid
        self.params = params
        self.bots = bots
        self.bot_locations = []
        for bot in self.bots:
            if (bot.location[0], bot.location[1]) not in self.bot_locations:
                self.bot_locations.append((bot.location[0], bot.location[1]))

        self.coverage = False
        self.dead = False
        for bot in self.bots:
            if bot.bot_type == BotType.scavenger:
                self.coverage = True
            elif bot.bot_type == BotType.morgue:
                self.dead = True

        self.obstacles = []
        if self.params.obstacles:
            self.generate_obstacles(random_=self.params.random_obstacles)
        self.casualties = []
        if self.params.casualties:
            self.generate_casualties(random_=self.params.random_obstacles)
        self.casualties_locations = [(casualty.x, casualty.y) for casualty in self.casualties]
        self.plot_grid()


    # generator random locations for casualties based on global parameter
    def generate_casualties(self, random_=True):
        if random_:
            for i in range(self.params.num_casualties):
                point = (round(random.random() * self.params.width, 2), round(random.random() * self.params.height, 2))
                # make sure that randomly generated point is not inside an obstacle
                while not self.container_checker(point):
                    point = (round(random.random() * self.params.width, 2), round(random.random() * self.params.height, 2))

                casualty_type = random.randint(0, 1)
                if self.dead:
                    if casualty_type == 0:
                        casualty_type = CasualtyType.injured
                    elif casualty_type == 1:
                        casualty_type = CasualtyType.dead
                else:
                    casualty_type = CasualtyType.injured

                if self.coverage:
                    self.casualties.append(Casualty([point[0], point[1]], casualty_type))
                else:
                    self.casualties.append(Casualty([point[0], point[1]], casualty_type, found=True, color='c'))
                # self.casualties.append([point[0], point[1], 'p', False])
        else:
            # manually added casualties for consistency during testing
            # casualties = [[1, 4], [2,3], [4, 8], [8, 2], [9, 7], [6,3], [6, 2], [5, 1], [3, 6], [5, 7]]
            casualties = [[5, 25], [3,6], [12, 15], [16, 28], [25, 6], [1,18], [29, 6], [4, 21], [16, 19], [2, 4]]
            # casualties = [[1, 4], [2,3], [4, 8], [8, 2], [9, 7]]
            for casualty in casualties:
                self.casualties.append(Casualty([casualty[0], casualty[1]], CasualtyType.injured))
                # self.casualties.append([casualty[0], casualty[1], 'p', False])


    # make sure obstacles do not overlap
    def container_checker(self, point):
        if isinstance(point, list):
            points = [(point[0][0], point[0][1]), (point[0][0] + self.params.obstacle_side_length, point[0][1]),
                                (point[0][0], point[0][1] + self.params.obstacle_side_length),
                                (point[0][0] + self.params.obstacle_side_length, point[0][1] + self.params.obstacle_side_length)]

            for p in points:
                p = Point(p[0], p[1])
                for obstacle in self.obstacles:
                    if obstacle.contains(p):
                        return False
                    if obstacle.intersects(p):
                        return False

        elif isinstance(point, tuple):
            p = Point(point[0], point[1])
            for obstacle in self.obstacles:
                if obstacle.contains(p):
                    return False
                if obstacle.intersects(p):
                    return False

        return True


    # generate random unit squares as obstacles
    ## TODO: make some of the obstacles triangles
    def generate_obstacles(self, random_=True):
        if random_:
            for i in range(self.params.num_obstacles):
                init = (round(random.random() * (self.params.width - self.params.obstacle_side_length), 2),
                            round(random.random() * (self.params.height - self.params.obstacle_side_length), 2))
                while not self.container_checker([init]):
                    init = (round(random.random() * (self.params.width - self.params.obstacle_side_length), 2),
                                round(random.random() * (self.params.height - self.params.obstacle_side_length), 2))
                # to make polygons other than boxes
                # r1 = sg.Polygon([(init[0], init[1]), (init[0], init[1] + 1), (init[0] + 1, init[1]), (init[0] + 1, init[1] + 1)])

                r1 = sg.box(init[0], init[1], init[0] + self.params.obstacle_side_length, init[1] + self.params.obstacle_side_length)
                self.obstacles.append(r1)

        else:
            # manually added obstacles for consistency during testing
            # obstacles = [[1, 5], [2,2], [1, 8], [4, 4], [8, 9], [6,6], [7, 4], [8, 8], [3, 8], [4, 6]]
            obstacles = [[4, 5], [2,8], [4, 19], [28, 4], [29, 16], [13,16], [2, 9], [19, 26], [24, 19], [8, 14]]
            # obstacles = [[1, 5], [2,2], [1, 8], [4, 4], [8, 9]]

            for obstacle in obstacles:
                r1 = sg.box(obstacle[0], obstacle[1], obstacle[0] + self.params.obstacle_side_length, obstacle[1] + self.params.obstacle_side_length)
                self.obstacles.append(r1)

        # make sure none of the obstacles are where the bots start
        for i, obstacle in enumerate(self.obstacles):
            for location in self.bot_locations:
                point = Point(location[0], location[1])
                if obstacle.contains(point):
                    self.obstacles.remove(obstacle)


    # plot only the casualties and obstacles
    def plot_grid(self):
        # set up the plot
        fig, ax = plt.subplots()
        points = []

        # plot casualties and their markers
        plt.axes(ax)
        for i in range(len(self.casualties)):
            plt.scatter(self.casualties[i].x, self.casualties[i].y, marker=self.casualties[i].marker, color=self.casualties[i].color)
        ax.set_aspect('equal', 'datalim')

        # plot obstacles
        for shape in self.obstacles:
            xs, ys = shape.exterior.xy
            ax.fill(xs, ys, alpha=0.5, fc='r', ec='none')

        ax.set_xlim((-1, self.params.x_max))
        ax.set_ylim((-1, self.params.y_max))
        plt.savefig("initial_grid.png")


    # TODO: create moving obstacles
    def shift_obstacles(self):

        x_change = 0
        y_change = 0

        def translation_validity_checker(obstacle):

            def overlap_checker(obstacle, xs, ys):
                for location in self.bot_locations:
                    location = Point(location[0], location[1])
                    if obstacle.contains(location):
                        return False

                for location in self.casualties_locations:
                    location = Point(location[0], location[1])
                    if obstacle.contains(location):
                        return False

                x = min(xs)
                y = min(ys)
                if not self.container_checker([(x, y)]):
                    return False

                return True

            def bounds_validity_checker(x, y):
                if x < self.params.x_min or x > self.params.x_max:
                    return False
                elif y < self.params.y_min or y > self.params.y_max:
                    return False
                return True

            xs, ys = obstacle.exterior.xy
            for i in range(len(xs)):
                if not bounds_validity_checker(xs[i], ys[i]):
                    return False

            if not overlap_checker(obstacle, xs, ys):
                return False

            return True

        def random_direction_generator():
            x_sign = random.randint(0, 1)
            y_sign = random.randint(0, 1)
            x = 0
            y = 0
            if x_sign and y_sign:
                x += random.random()
                y += random.random()
            elif x_sign and not y_sign:
                x += random.random()
                y -= random.random()
            elif not x_sign and y_sign:
                x -= random.random()
                y += random.random()
            else:
                x -= random.random()
                y -= random.random()
            return x * self.params.obstacle_max_shift, y * self.params.obstacle_max_shift


        def translate(x, y):
            return x + x_change, y + y_change


        for i in range(len(self.obstacles)):
            shift = random.random()
            if shift < self.params.moving_obstacle_probability:
                obstacle = self.obstacles[i]

                copy_ = copy.deepcopy(obstacle)
                x_change, y_change = random_direction_generator()
                copy_ = so.transform(translate, copy_)
                while not translation_validity_checker(copy_):
                    x_change, y_change = random_direction_generator()
                    copy_ = so.transform(translate, copy_)

                self.obstacles[i] = copy_
