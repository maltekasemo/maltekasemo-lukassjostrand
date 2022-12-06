from Lab1.tramdata import *
from graphs import *
import json
TRAM_FILE = 'tramnetwork.json'

with open(TRAM_FILE, 'r') as data:
    cheat = json.load(data)

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
        self._position = (lat, lon)

class TramLine: #CHECK
    def __init__(self, num: str, stops: list):
        self._number = num
        self._stops = stops

    def get_number(self): #CHECK
        return self._number

    def get_stops(self): #CHECK
        return self._stops

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

    def geo_distance(self, a, b): #NJA-CHECK
        return distance_between_stops(cheat['stops'], self._stopdict[a], self._stopdict[b])

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

def readTramnetwork(file = TRAM_FILE): #CHECK
    with open(file, 'r') as data:
        tramnetwork = json.load(data)

    dict_of_stops = {stop: TramStops(stop, lines_via_stop(tramnetwork['lines'], stop), tramnetwork['stops'][stop]['lat'],
                         tramnetwork['stops'][stop]['lon']) for stop in tramnetwork['stops']}

    dict_of_lines = {}
    for line in tramnetwork['lines']:
        dict_of_lines[line] = TramLine(line, [dict_of_stops[stop] for stop in tramnetwork['lines'][line]])

    return TramNetwork(dict_of_lines, dict_of_stops, tramnetwork['times'])

def getting_objects_by_names(G, src, trg):
    all_stops = G.all_stops()
    for stop in all_stops:
        if stop._name == src:
            source = stop
        elif stop._name == trg:
            target = stop
    return source, target

def demo():
    G = readTramnetwork(TRAM_FILE)
    try:
        src, trg = input('Please use format <source>,<target> <> ').split(',')
    except ValueError:
        print('Try again')
        exit()

    try:
        source, target = getting_objects_by_names(G, src, trg)
        view_shortest(G, source, target)
    except UnboundLocalError:
        print('Unknown argument(s)')

if __name__ == '__main__':
    demo()











