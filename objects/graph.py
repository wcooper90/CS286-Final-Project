from .graph_node import GraphNode
import shapely.geometry
import matplotlib.pyplot as plt
import os
import math


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
                    bool = self.edge_validity_checker(start, end)
                    if bool:
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
            plt.plot(*edge[0].xy)

        plt.savefig(os.getcwd() + "/graph.png")


    def edge_validity_checker(self, start, end):
        line = shapely.geometry.LineString([start, end])
        for obstacle in self.obstacles:
            if line.crosses(obstacle):
                return False
            if obstacle.contains(line):
                return False

        self.edges.append([line, line.length, end])
        return True



    def sample_based_graph_construction(self):
        pass


    def update_graph(self):
        pass


    def update_bots(self):
        pass


    def dijkstras(self, init, end):

        def minDistance(dist, sptSet):
            min_ = 1e7
            min_index = 1e7

            for v in range(len(self.graph)):
                if dist[v] < min_ and sptSet[v] == False:
                    min_ = dist[v]
                    min_index = v

            return min_index

        def checkExistance(init, end):
            node1edges = [node.location for node in self.graph[init].edges]
            node1location = self.graph[init].location
            node2location = self.graph[end].location
            for edge in node1edges:
                if node2location == edge:
                    return math.dist(node1location, node2location)
            return False

        num_vertices = len(self.graph)
        dist = [1e7] * num_vertices
        prev = [None] * num_vertices

        start = None
        for i, node in enumerate(self.graph):
            if node.location == init:
                start = i
            if node.location == end:
                end = i

        dist[start] = 0
        sptSet = [False] * num_vertices

        for _ in range(num_vertices):

            # if dist[end] < 1e7:
            #     break

            u = minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(num_vertices):
                length = checkExistance(u, v)
                # print(length)
                if length:
                    if sptSet[v] == False and dist[v] > dist[u] + length:
                        dist[v] = dist[u] + length
                        prev[v] = u

        curr = end
        steps = []
        while curr != start:
            steps.insert(0, self.graph[curr].location)
            curr = prev[curr]

        return steps
