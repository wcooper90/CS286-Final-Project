from objects.enum import PlanningAlgorithmType


class Globals():

    # plot parameters
    width = 50
    height = 50
    res = 1
    x_min = 0
    y_min = 0
    x_max = width + 2
    y_max = height + 2

    # booleans
    casualties = True
    obstacles = True
    random_obstacles = True
    random_casualties = True
    plot_data = True

    # number of obstacles and casualties
    num_obstacles = 50
    num_casualties = 100

    # size of obstacles
    obstacle_side_length = 3

    # total iterations allowed
    time = 400

    # minimum distance from a casualty a bot has to be for it to be considered reached
    min_dist_from_casualty = 0.1

    scavenger_bot_sensing_radius = 7

    # strictly greedy policy
    planning_algorithm = None

    # Probablistic Sampling Method
    planning_algorithm = PlanningAlgorithmType.PSM

    PSM_density = 0.1
    # Rapidly-Exploring Random Tree
    # planning_algorithm = PlanningAlgorithmType.RRT

    # Global Dijkstra's
    # planning_algorithm = PlanningAlgorithmType.Global_Dijkstra
