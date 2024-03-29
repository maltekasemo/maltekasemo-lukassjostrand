# TODO: mock-up to be replaced by your file from Lab 2

class Graph():
    def __init__(self, edgelist: list = None):
        super().__init__()
        self._engine = 'neato'
        self._adjlist = {}
        self._valuelist = {}
        if edgelist:
            self.init_using_edgelist(edgelist)

    def init_using_edgelist(self, edgelist):
        for tuple in edgelist:
            self.add_edge(tuple[0], tuple[1])
            self.add_vertex(tuple[0])
            self.add_vertex(tuple[1])

    def __len__(self):
        return len(self._adjlist)

    def add_edge(self, a, b):
        if a in self._adjlist:
            if b not in self._adjlist[a]:
                self._adjlist[a].append(b)
        else:
            self._adjlist[a] = [b]
        if b in self._adjlist:
            if a not in self._adjlist[b]:
                self._adjlist[b].append(a)
        else:
            self._adjlist[b] = [a]

    def add_vertex(self, a):
        if a not in self._valuelist:
            self._valuelist[a] = None
        if a not in self._adjlist:
            self._adjlist[a] = []

    def edges(self):
        edges = []
        for vertex, neighbours in self._adjlist.items():
            for neighbour in neighbours:
                if (vertex, neighbour) not in edges and (neighbour, vertex) not in edges:
                    edges.append((vertex, neighbour))
        return edges

    def get_vertex_value(self, v):
        return self._valuelist[v]

    def neighbours(self, v):
        return [neighbour for neighbour in self._adjlist[v]]

    def remove_edge(self, a, b):
        if a in self._adjlist:
            if b in self._adjlist[a]:
                self._adjlist[a].remove(b)
        if b in self._adjlist:
            if a in self._adjlist[b]:
                self._adjlist[b].remove(a)

    def remove_vertex(self, v):
        self._adjlist.pop(v)
        for item in self._adjlist:
            if v in self._adjlist[item]:
                self._adjlist[item].remove(v)
        self._valuelist.pop(v)

    def set_vertex_value(self, v, x):
        self._valuelist[v] = x

    def vertices(self):
        return [vertice for vertice in self._valuelist]

class WeightedGraph(Graph):
    def __init__(self, edgelist=None):
        super().__init__(edgelist)
        self._weightlist = {}

    def get_weight(self, a, b):
        try:
            return self._weightlist[(a, b)]
        except KeyError:
            return self._weightlist[(b, a)]

    def set_weight(self, a, b, w):
        self._weightlist[(a, b)] = w


def dijkstra(graph, source, cost=lambda u, v: 1):
    path_to_stop = {v: 9999 for v in graph.vertices()}
    previous_stops = {previous: None for previous in graph.vertices()}
    path_to_stop[source] = 0
    unseen_vertices = [v for v in graph.vertices()]

    while unseen_vertices:
        max_time = {v: path_to_stop[v] for v in unseen_vertices}
        u = min(max_time, key=max_time.get)
        unseen_vertices.remove(u)

        for neighbour in graph.neighbours(u):
            alt_path = path_to_stop[u] + cost(u, neighbour)
            if alt_path < path_to_stop[neighbour]:
                path_to_stop[neighbour] = alt_path
                previous_stops[neighbour] = u

    keys = list(previous_stops.keys())
    paths = {}

    for i in previous_stops.keys():
        path = [i]
        for key in keys:
            while key != i and path[-1] is not None:
                path.append(previous_stops[path[-1]])
        path.pop()
        paths[i] = path

    paths_with_time = {stop: {'path': paths[stop], 'dist': None} for stop in paths}
    for stop in path_to_stop:
        paths_with_time[stop]['dist'] = path_to_stop[stop]

    return paths_with_time

def getting_objects_by_names(G, dep, dest):
    all_stops = G.all_stops()
    for stop in all_stops:
        if stop._name == dep:
            departure = stop
        elif stop._name == dest:
            destination = stop
    return departure, destination