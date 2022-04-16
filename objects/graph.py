from .graph_node import GraphNode
import shapely.geometry
import matplotlib.pyplot as plt
import os
import math


class Graph():
    def __init__(self, casualties, obstacles, bots):
        # driver function, creates and plots the graph
        self.obstacles = obstacles
        self.casualties = casualties
        self.bots = bots
        self.edges = []

        # this is just a collection of vertex nodes
        self.graph = self.construct_vertices()
        self.plot_graph()


    # construct the vertex nodes of the graph
    def construct_vertices(self):
        vertices = []

        # append all corners of convex obstacles to vertex locations
        for obstacle in self.obstacles:
            x, y = obstacle.exterior.coords.xy
            for i in range(len(x)):
                vertices.append(GraphNode([x[i], y[i]], 'obstacle'))

        # append all casualty locations to vertex locations
        for casualty in self.casualties:
            vertices.append(GraphNode([casualty[0], casualty[1]], 'casualty'))

        # append all bot locations to vertex locations
        for bot in self.bots:
            vertices.append(GraphNode([bot.location[0], bot.location[1]], 'bot'))

        # connect all edges based on existed vertices and return
        self.construct_edges(vertices)
        return vertices


    # construct edges between vertices
    def construct_edges(self, vertices):

        # assume fully connected graph
        for i in range(len(vertices)):
            start = vertices[i].location
            for j in range(len(vertices)):

                # vertices don't loop to themselves
                if i == j:
                    continue
                else:
                    end = vertices[j].location
                    # make sure edges don't cross through obstacles
                    if self.edge_validity_checker(start, end):
                        vertices[i].edges.append(vertices[j])


    # plot the vertices and edges
    def plot_graph(self):

        # scatter nodes
        fig, ax = plt.subplots()
        x = []
        y = []
        for node in self.graph:
            x.append(node.location[0])
            y.append(node.location[1])
        plt.scatter(x, y)

        # plot edges (Line objects)
        for edge in self.edges:
            plt.plot(*edge[0].xy)

        plt.savefig(os.getcwd() + "/graph.png")


    # check if a proposed edge is legitimate
    def edge_validity_checker(self, start, end):
        line = shapely.geometry.LineString([start, end])
        for obstacle in self.obstacles:
            # line cannot cross the edge of an obstacle
            if line.crosses(obstacle):
                return False
            # line cannot be contained by an obstacle
            if obstacle.contains(line):
                return False

        # keep an internal track of edges
        self.edges.append([line, line.length, end])
        return True



    def sample_based_graph_construction(self):
        pass


    def update_graph(self):
        pass


    def update_bots(self):
        pass


    # Dijkstra's algorithm to find fastest paths between obstacles for bots
    def dijkstras(self, init, end):

        # finds the minimum distance next node which we haven't already visited
        def minDistance(dist, sptSet):
            min_ = 1e7
            min_index = 1e7
            for v in range(len(self.graph)):
                if dist[v] < min_ and sptSet[v] == False:
                    min_ = dist[v]
                    min_index = v
            return min_index

        # check to see if there is an edge between two proposed nodes
        def checkExistance(init, end):
            node1edges = [node.location for node in self.graph[init].edges]
            node1location = self.graph[init].location
            node2location = self.graph[end].location
            for edge in node1edges:
                if node2location == edge:
                    return math.dist(node1location, node2location)
            return False

        # initialize metadata arrays
        num_vertices = len(self.graph)
        dist = [1e7] * num_vertices
        # keep track of the last node in a path, so we can retrace our steps to find the shortest path
        prev = [None] * num_vertices

        # find the index number of the start and ending nodes
        start = None
        for i, node in enumerate(self.graph):
            if node.location == init:
                start = i
            if node.location == end:
                end = i

        dist[start] = 0
        sptSet = [False] * num_vertices

        # iterate through all points, find next minimum distance
        for _ in range(num_vertices):
            u = minDistance(dist, sptSet)
            sptSet[u] = True
            # then look for the minimum distance node's edge existance and update parameters
            for v in range(num_vertices):
                length = checkExistance(u, v)
                if length:
                    if sptSet[v] == False and dist[v] > dist[u] + length:
                        dist[v] = dist[u] + length
                        prev[v] = u

        # use the prev array to find the forwards progression of next steps for a bot,
        # converted from node index numbers to the respective nodes' locations
        curr = end
        steps = []
        while curr != start:
            steps.insert(0, self.graph[curr].location)
            curr = prev[curr]

        # return a sequence of steps the bot will take 
        return steps
