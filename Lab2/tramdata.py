import sys
from math import sin, cos, sqrt, atan2, pi
import json
import csv

STOPS_JSON_FILE = 'tramstops.json'
TRAMLINES_TSV_FILE = 'tramlines.txt'

def get_open_json_file():
    infile = 'tramnetwork.json'
    with open(infile, 'r') as data:
        tramnetwork = json.load(data)
    return tramnetwork

##-----------------------------MAIN FUNCTION-------------------------------

def dialogue():
    running = True
    print("The following formats are functioning:\nvia <stop>\nbetween <stop1> and <stop2>"
            "\ntime with <line> from <stop1> to <stop2>\ndistance from <stop1> to <stop2>\nquit")
    while running:
        input_string = input("> ")
        if input_string == 'quit':
            print("Bye bye!")
            running = False
            continue
        else:
            if "via" in input_string:
                query = "lines passing stop"
                answer = answer_query(input_string, query)
            elif 'between' in input_string and 'and' in input_string:
                query = 'lines between stops'
                answer = answer_query(input_string, query)
            elif 'time with' in input_string and 'from' in input_string and 'to' in input_string:
                query = 'time from a to b'
                answer = answer_query(input_string, query)
            elif 'distance from' in input_string and 'to' in input_string:
                query = 'distance from a to b'
                answer = answer_query(input_string, query)
            else:
                print("Sorry, try again!")
                answer = None
        if answer:
            print(answer)

##-----------------------------ADAPTING STRING AND ACTIVIATING CALCULATING METHODS-------------------------------

def answer_query(input_string, query):
    tramnetwork = get_open_json_file()
    if query == 'lines passing stop':
        stop = input_string.split('via ')[1]
        if input_string.split('via ')[0]:
            return 'Sorry, try again'
        stop.lstrip().rstrip()
        answer = lines_via_stop(tramnetwork['lines'], stop)
    elif query == 'lines between stops':
        stop1_and_stop2 = input_string.split('between')[1]
        stops = stop1_and_stop2.split(' and ')
        stop1 = stops[0].lstrip().rstrip()
        stop2 = stops[1].lstrip().rstrip()
        answer = lines_between_stops(tramnetwork['lines'], stop1, stop2)
    elif query == 'time from a to b':
        try:
            line_and_stops = input_string.lstrip('time with ')
            line = line_and_stops.split('from')[0].lstrip().rstrip()
            stops = line_and_stops.split('from')[1]
            stop1 = stops.split(' to ')[0].lstrip().rstrip()
            stop2 = stops.split(' to ')[1].lstrip().rstrip()
        except IndexError:
            return "Sorry, try again"
        answer = time_between_stops(tramnetwork, line, stop1, stop2)
    elif query == 'distance from a to b':
        stop1_and_stop2 = input_string.lstrip('distance from')
        stops = stop1_and_stop2.split(' to ')
        stop1 = stops[0].rstrip().lstrip()
        stop2 = stops[1].rstrip().lstrip()
        answer = distance_between_stops(tramnetwork['stops'], stop1, stop2)
    return answer

##-----------------------------CALCULATING METHODS-------------------------------

def lines_via_stop(lines_dict, stop):
    lines_via_stop = [line for line in lines_dict if stop in lines_dict[line]]
    if lines_via_stop:
        return lines_via_stop
    else:
        return "Unknown argument(s)"

def lines_between_stops(lines_dict, stop1, stop2):
    lines_between_stops = [line for line in lines_dict if stop1 in lines_dict[line] and stop2 in lines_dict[line]]
    if lines_between_stops:
        return lines_between_stops
    else:
        return "Unknown argument(s)"

def time_between_stops(tramnetwork, line, stop1, stop2):
    try:
        start_index = tramnetwork['lines'][line].index(stop1)
        end_index = tramnetwork['lines'][line].index(stop2)

        if start_index > end_index:
            start_index, end_index = end_index, start_index

        stations_between_stops = [tramnetwork['lines'][line][i] for i in range(start_index, end_index + 1)]
        time = 0

        for i in range(len(stations_between_stops)-1):
            time += tramnetwork['times'][stations_between_stops[i]][stations_between_stops[i + 1]]
        return time

    except ValueError:
        return "Unknown argument(s)"

def distance_between_stops(positions_dict, stop1, stop2):
    try:
        lon1 = positions_dict[stop1]["lon"] * pi / 180
        lon2 = positions_dict[stop2]["lon"] * pi / 180
        lat1 = positions_dict[stop1]["lat"] * pi / 180
        lat2 = positions_dict[stop2]["lat"] * pi / 180

        R = 6371.0

        lon_diff = abs(lon1 - lon2)
        lat_diff = abs(lat1 - lat2)

        a = (sin(lat_diff / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(lon_diff / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return round(distance, 4)

    except KeyError:
        return "Unknown argument(s)"

##-----------------------------READING TEXT-FILE AND ADAPTING TO USAGE-------------------------------

def reading_tsv_file(text_file):
    tsv_read = {}
    stops_and_times_in_line = {}
    with open(text_file) as file:
        rows = csv.reader(file, delimiter="\t")
        for line in rows:
            if not line:
                tsv_read[temp_var] = stops_and_times_in_line.copy()
                stops_and_times_in_line = {}
            elif len(line[0]) <= 3 and len(line[0]) > 0:
                temp_var = line[0].rstrip(":")
            else:
                try:
                    the_split = line[0].rsplit(" ", 1)
                    name = (the_split[0]).rstrip()
                    stops_and_times_in_line[name] = the_split[1]
                except IndexError:
                    pass
        tsv_read[temp_var] = stops_and_times_in_line.copy()
    return tsv_read

##-----------------------------CREATING THE THREE DICTIONARIES INDEPENDENTLY-------------------------------

def creating_lines(tsv_read):
    return {line: [stop for stop in tsv_read[line]] for line in tsv_read}

def creating_neighbours(lines_dict, tsv_read):
    out_dict = {}
    for line_stops in lines_dict.values():
        for i in range(len(line_stops)-1):
            if line_stops[i] not in out_dict.keys():
                out_dict[line_stops[i]] = {line_stops[i+1]: time_distance(tsv_read, line_stops[i], line_stops[i+1])}
            else:
                out_dict[line_stops[i]][line_stops[i+1]] = time_distance(tsv_read, line_stops[i], line_stops[i+1])
    return out_dict

def build_trams_stops(tramstops):
    with open(tramstops, 'r') as infile:
        all_stops = json.load(infile)
        return {stop: {"lat": float(all_stops[stop]["position"][0]), "lon": float(all_stops[stop]["position"][1])} for stop in all_stops}

##-----------------------------METHODS USED BY CREATING NEIGHBOURS-------------------------------

def time_distance(times_dict, stop1, stop2):
    for line in times_dict:
        try:
            minutes1 = convert(times_dict[line][stop1])
            minutes2 = convert(times_dict[line][stop2])
            return abs(minutes1 - minutes2)
        except KeyError:
            continue

def convert(time):
    minutes = time.split(":")
    return int(minutes[1])

##-----------------------------CREATION AND FUSION OF THREE DICTIONARIES-------------------------------

def collect_all_data(jsonfile, tsv_file):
    tramnetwork = {}
    tsv_read = reading_tsv_file(tsv_file)
    stops = build_trams_stops(jsonfile)
    lines = creating_lines(tsv_read)
    times = creating_neighbours(lines, tsv_read)
    tramnetwork['stops'] = stops
    tramnetwork['lines'] = lines
    tramnetwork['times'] = times
    return tramnetwork

def create_json_file(tramnetwork, filename ="tramnetwork.json"):
    with open(filename, 'w') as f:
        json.dump(tramnetwork, f, indent=2, ensure_ascii=False)
        f.close()

##-----------------------------CREATING JSON FILE-------------------------------

def build_tram_network():
    tramnetwork = collect_all_data(STOPS_JSON_FILE, TRAMLINES_TSV_FILE)
    create_json_file(tramnetwork)

##-----------------------------CONTROLLING THE PROGRAM FLOW-------------------------------

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network()
    else:
        dialogue()



