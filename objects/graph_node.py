class GraphNode():
    # basic graph node 
    def __init__(self, location, type):
        self.location = location
        self.edges = []
        self.type = type
