# visualization of shortest path in Lab 3, modified to work with Django
#from extra import extraGraph
from tram.utils.trams import readTramNetwork
from tram.utils.graphs import *
from .color_tram_svg import color_svg_network
import os
from django.conf import settings


def show_shortest(dep, dest):
    network = readTramNetwork()
    departure, destination = getting_objects_by_names(network, dep, dest)
    quickest_path = dijkstra(network, departure, network.get_weight)[destination]['path']
    quickest_path_time = dijkstra(network, departure, network.get_weight)[destination]['dist']

    qp = []
    for object in quickest_path:
        qp.append(object._name)
    qp.reverse()

    shortest_path = dijkstra(network, departure, network.geo_distance)[destination]['path']
    shortest_path_distance = dijkstra(network, departure, network.geo_distance)[destination]['dist']
    shortest_path_distance = round(shortest_path_distance, 2)

    sp = []
    for object in shortest_path:
        sp.append(object._name)
    sp.reverse()


    # First you need to calculate the shortest and quickest paths, by using appropriate
    # cost functions in dijkstra().
    # Then you just need to use the lists of stops returned by dijkstra()
    #
    # If you do Bonus 1, you could also tell which tram lines you use and where changes
    # happen. But since this was not mentioned in lab3.md, it is not compulsory.

    shortest = [departure, 'Chalmers', destination]

    timepath = 'Quickest: ' + ', '.join(qp) + ', ' + str(quickest_path_time)
    geopath = 'Shortest: ' + ', '.join(sp) + ', ', str(shortest_path_distance)

    def colors(v):
        if v in qp and v in sp:
            return 'cyan'
        elif v in qp:
            return 'orange'
        elif v in sp:
            return 'green'
        else:
            return 'white'


    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath
