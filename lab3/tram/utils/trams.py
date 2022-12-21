import json

# imports added in Lab3 version
import math
import os
from tram.utils.graphs import WeightedGraph
from django.conf import settings


# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here
TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')
with open(TRAM_FILE, 'r') as data:
    cheat = json.load(data)


# TODO: use your lab 2 class definition, but add one method
class TramLine: #CHECK
    def __init__(self, num: str, stops: list):
        self._number = num
        self._stops = stops

    def get_number(self): #CHECK
        return self._number

    def get_stops(self): #CHECK
        return self._stops

class TramStops: #CHECK
    def __init__(self, name: str, lines: list, lat: float, lon: float):
        self._lines = lines
        self._name = name
        self._position = (lon, lat)

    def add_line(self, line): #CHECK
        self._lines.append(line)

    def get_lines(self): #CHECK
        return self._lines

    def get_name(self): #CHECK
        return self._name

    def get_position(self): #CHECK
        return self._position

    def set_position(self, lat: float, lon: float): #CHECK
        self._position = (lon, lat)

class TramNetwork(WeightedGraph):
    def __init__(self, lines: dict, stops: dict, times: dict, edgelist: list = None):
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times
        if edgelist is None:
            all_edges = []
            all_lines = self.all_lines()
            for line in all_lines:
                line_edge_list = [(all_lines[line].get_stops()[i], all_lines[line].get_stops()[i + 1]) for i in
                                  range(len(all_lines[line].get_stops()) - 1) if (all_lines[line].get_stops()[i], all_lines[line].get_stops()[i + 1]) not in all_edges]
                all_edges += line_edge_list
            super().__init__(edgelist= all_edges)
            self._weightlist = {edge: self.transition_time(edge[0], edge[1]) for edge in self.edges()}
        else:
            super().__init__(edgelist=edgelist)
            self._weightlist = {edge: self.transition_time(edge[0], edge[1]) for edge in self.edges()}

    def all_lines(self): #CHECK
        return {line: self._linedict[line] for line in self._linedict}

    def all_stops(self): #CHECK
        return [self._stopdict[stop] for stop in self._stopdict]

    def extreme_position(self): #CHECK
        lat_list = [self._stopdict[stop]._position[0] for stop in self._stopdict]
        lon_list = [self._stopdict[stop]._position[1] for stop in self._stopdict]
        return (max(lat_list), max(lon_list), min(lat_list), min(lon_list))

    def geo_distance(self, a, b):
            try:
                lon1 = a.get_position()[0] * pi / 180
                lon2 = b.get_position()[0] * pi / 180
                lat1 = a.get_position()[1] * pi / 180
                lat2 = b.get_position()[1] * pi / 180

                R = 6371.0

                lon_diff = abs(lon1 - lon2)
                lat_diff = abs(lat1 - lat2)

                a = (sin(lat_diff / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(lon_diff / 2)) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                return round(distance, 4)
            except KeyError:
                return None

    def line_stops(self, line): #CHECK
        return [stop for stop in self._linedict[line].get_stops()]

    def remove_lines(self, lines): #CHECK
        for line in lines:
            self._linedict.pop(line)

    def stop_lines(self, a): #CHECK
        return self._stopdict[a].get_lines()

    def stop_position(self, a): #CHECK
        return self._stopdict[a].get_position()

    def transition_time(self, a, b): #CHECK
        try:
            return self._timedict[a.get_name()][b.get_name()]
        except KeyError:
            try:
                return self._timedict[b.get_name()][a.get_name()]
            except KeyError:
                return None

    def extreme_positions(self):
        stops = self._stopdict.values()
        minlat = min([s._position[0] for s in stops])
        minlon = min([s._position[1] for s in stops])
        maxlat = max([s._position[0] for s in stops])
        maxlon = max([s._position[1] for s in stops])

        return minlon, minlat, maxlon, maxlat
    
def lines_via_stop(lines_dict, stop):
    lines_via_stop = [line for line in lines_dict if stop in lines_dict[line]]
    if lines_via_stop:
        return lines_via_stop

def readTramNetwork(file = TRAM_FILE): #CHECK
    with open(file, 'r') as data:
        tramnetwork = json.load(data)

    dict_of_stops = {stop: TramStops(stop, lines_via_stop(tramnetwork['lines'], stop), tramnetwork['stops'][stop]['lat'],
                         tramnetwork['stops'][stop]['lon']) for stop in tramnetwork['stops']}

    dict_of_lines = {}
    for line in tramnetwork['lines']:
        dict_of_lines[line] = TramLine(line, [dict_of_stops[stop] for stop in tramnetwork['lines'][line]])

    return TramNetwork(dict_of_lines, dict_of_stops, tramnetwork['times'])


# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified

    """lines_via_stop = [line for line in network['lines'] if stop in network['lines'][line]]
    #append lines_via_stop to every stop

    lines_between_stops = [line for line in network['lines'] if stop1 in network['lines'][line] and stop2 in network['lines']
    #add edge for every line that serves between a and b"""

    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance

