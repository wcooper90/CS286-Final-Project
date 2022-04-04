from objects.bot import Bot


class Globals():

    def generate_bots(self, coordinates):
        robots = []
        for coordinate in coordinates:
            robots.append(Bot(coordinate))

        return robots


    self.width = 10
    self.height = 10
    self.res = 1
    self.robot_coordinates = [[5, 1], [4, 8], [9, 3], [1, 6]]
    self.num_robots = len(self.robot_coordinates)
    self.robots = self.generate_bots(self.robot_coordinates)


    self.casualties = True
    self.obstacles = False 
