import networkx as nx
import haversine as hs
import matplotlib.pyplot as plt
import sklearn.cluster as sk
import numpy as np
import sys

AIRPORTS_FILE = 'airports.dat'
ROUTES_FILE = 'routes.dat'

def mk_airportdict(FILE):
    all_airports = {}
    with open(FILE) as file:
        rows = file.readlines()
        for line in rows:
            try:
                id = str(line.split(',')[0])
                name = str(line.split(',')[1].strip('"'))
                lon = float(line.split(',')[7])
                lat = float(line.split(',')[6])
                all_airports[id] = {'name': name, 'lon': lon, 'lat': lat}
            except ValueError:
                pass

    return all_airports

def mk_routeset(FILE):
    id = 0
    all_routes = {}
    with open(FILE) as file:
        rows = file.readlines()
        for line in rows:
            try:
                id += 1
                if line.split(',')[3] != '\\N':
                    departing = str(line.split(',')[3])
                if line.split(',')[5] != '\\N':
                    arriving = str(line.split(',')[5])
                all_routes[id] = {'departing': departing, 'arriving': arriving}
            except ValueError:
                pass

    return all_routes

def mk_routegraph(all_airports, routeset):
    route_graph = nx.Graph()

    for airport in all_airports:
        route_graph.add_node(airport, lat =all_airports[airport]['lat'], lon = all_airports[airport]['lon'])
    for route in routeset:
        try:
            departing_coords = (all_airports[routeset[route]['departing']]['lat'], all_airports[routeset[route]['departing']]['lon'])
            arriving_coords = (all_airports[routeset[route]['arriving']]['lat'], all_airports[routeset[route]['arriving']]['lon'])
            route_graph.add_edge(routeset[route]['departing'], routeset[route]['arriving'])
            route_graph.edges[routeset[route]['departing'], routeset[route]['arriving']]['weight'] = hs.haversine(departing_coords, arriving_coords, normalize=True, unit='km')
        except KeyError:
            pass

    return route_graph

def k_spanning_tree(G, k = 1000):
    edges = nx.algorithms.tree.mst.minimum_spanning_edges(G)
    edges_without_k_longest = [i for i in edges][:-k]

    lat = [G.nodes[node]['lat'] for node in G.nodes]
    lon = [G.nodes[node]['lon'] for node in G.nodes]

    plt.figure(figsize=(16, 10))
    plt.scatter(lon, lat, s=2)

    for edge in edges_without_k_longest:
        connected_lats = [G.nodes[edge[0]]['lat'], G.nodes[edge[1]]['lat']]
        connected_lons = [G.nodes[edge[0]]['lon'], G.nodes[edge[1]]['lon']]
        plt.plot(connected_lons, connected_lats, linewidth=2, alpha = 0.8)

    plt.show()

def k_means(data, k = 7):
    i = 0
    plt.figure(figsize=(16, 10))
    kmeans = sk.KMeans(n_clusters = k).fit(data)
    colors = "ygrkmbc"
    for label in kmeans.labels_:
        plt.scatter(data[i][1], data[i][0], s=2, color=colors[label])
        i+=1
    plt.show()

def plot_airports(graph):
    plt.figure(figsize=(16, 10))
    lat = [graph.nodes[node]['lat'] for node in graph.nodes]
    lon = [graph.nodes[node]['lon'] for node in graph.nodes]
    plt.scatter(lon, lat, s=3)
    plt.show()

def plot_airports_and_routes(G):
    plt.figure(figsize=(16, 10))
    lat = [G.nodes[node]['lat'] for node in G.nodes]
    lon = [G.nodes[node]['lon'] for node in G.nodes]
    plt.scatter(lon, lat, s=3)

    for edge in G.edges():
        connected_lats = [G.nodes[edge[0]]['lat'], G.nodes[edge[1]]['lat']]
        connected_lons = [G.nodes[edge[0]]['lon'], G.nodes[edge[1]]['lon']]
        plt.plot(connected_lons, connected_lats, linewidth=0.25)
    plt.show()

if __name__ == '__main__':
    airports = mk_airportdict(AIRPORTS_FILE)
    routes = mk_routeset(ROUTES_FILE)
    routegraph = mk_routegraph(airports, routes)
    if sys.argv[1] == 'airports':
        plot_airports(routegraph)
    elif sys.argv[1] == 'routes':
        plot_airports_and_routes(routegraph)
    elif sys.argv[1] == 'span':
        k_spanning_tree(routegraph)
    elif sys.argv[1] == 'means':
        lat = [routegraph.nodes[node]['lat'] for node in routegraph.nodes()]
        lon = [routegraph.nodes[node]['lon'] for node in routegraph.nodes()]
        k_means(np.array([lat, lon]).T)
    else:
        print('Try again')
