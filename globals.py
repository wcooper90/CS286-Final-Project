from objects.enum import PlanningAlgorithmType


class Globals():

    # plot parameters
    width = 15
    height = 15
    res = 1
    x_min = 0
    y_min = 0

    # booleans
    casualties = True
    obstacles = True
    random_obstacles = True
    random_casualties = True
    plot_data = True

    # moving obstacles
    moving_obstacles = True
    moving_obstacle_probability = 0.3

    # obstacles will move with the above probability for every batch of the below iterations
    obstacle_shift_frequency = 10

    # obstacles' movement in the x or y direction is uniformly distributed from 0 to the below
    obstacle_max_shift = 1

    # number of obstacles and casualties
    num_obstacles = 5
    num_casualties = 15

    # size of obstacles
    obstacle_side_length = 2

    x_max = width + obstacle_side_length + 1
    y_max = height + obstacle_side_length + 1

    # total iterations allowed
    time = 200

    # minimum distance from a casualty a bot has to be for it to be considered reached
    min_dist_from_casualty = 0.1

    scavenger_bot_sensing_radius = 7

    graph_number = 0

    # strictly greedy policy
    planning_algorithm = None

    # Probablistic Sampling Method
    planning_algorithm = PlanningAlgorithmType.PSM

    PSM_density = 0.05
    # Rapidly-Exploring Random Tree
    # planning_algorithm = PlanningAlgorithmType.RRT

    # Global Dijkstra's
    # planning_algorithm = PlanningAlgorithmType.Global_Dijkstra
