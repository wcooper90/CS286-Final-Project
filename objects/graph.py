from .graph_node import GraphNode
import shapely.geometry
import matplotlib.pyplot as plt
import os


class Graph():
    def __init__(self, casualties, obstacles, bots):
        self.obstacles = obstacles
        self.casualties = casualties
        self.bots = bots
        self.edges = []
        self.graph = self.construct_vertices()

        self.plot_graph()


    def construct_vertices(self):
        vertices = []
        for obstacle in self.obstacles:
            x, y = obstacle.exterior.coords.xy
            for i in range(len(x)):
                vertices.append(GraphNode([x[i], y[i]], 'obstacle'))

        for casualty in self.casualties:
            vertices.append(GraphNode([casualty[0], casualty[1]], 'casualty'))

        for bot in self.bots:
            vertices.append(GraphNode([bot.location[0], bot.location[1]], 'bot'))

        self.construct_edges(vertices)

        return vertices


    def construct_edges(self, vertices):
        for i in range(len(vertices)):
            start = vertices[i].location
            for j in range(len(vertices)):
                if i == j:
                    continue
                else:
                    end = vertices[j].location
                    if self.edge_validity_checker(start, end):
                        vertices[i].edges.append(vertices[j])


    def plot_graph(self):
        fig, ax = plt.subplots()
        x = []
        y = []

        for node in self.graph:
            x.append(node.location[0])
            y.append(node.location[1])

        plt.scatter(x, y)

        for edge in self.edges:
            plt.plot(*edge.xy)

        plt.savefig(os.getcwd() + "/graph.png")


    def edge_validity_checker(self, start, end):
        line = shapely.geometry.LineString([start, end])
        for obstacle in self.obstacles:
            if line.crosses(obstacle):
                return False
            if obstacle.contains(line):
                return False

        self.edges.append(line)
        return True



    def sample_based_graph_construction(self):
        pass


    def update_graph(self):
        pass


    def update_bots(self):
        pass


    def dijkstras(self, init, end):
        pass
