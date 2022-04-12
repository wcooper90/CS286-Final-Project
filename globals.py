from objects.bot import Bot


class Globals():

    def generate_bots(self, coordinates):
        robots = []
        for coordinate in coordinates:
            robots.append(Bot(coordinate))

        return robots


    width = 10
    height = 10
    res = 1
    robot_coordinates = [[5, 1], [4, 8], [9, 3], [1, 6]]
    num_robots = len(robot_coordinates)
    # robots = generate_bots(robot_coordinates)
    x_min = 0
    y_min = 0
    x_max = 10
    y_max = 10


    casualties = True
    obstacles = False
    num_obstacles = 5
    num_casualties = 10
