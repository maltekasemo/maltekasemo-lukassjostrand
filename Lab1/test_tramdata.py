import unittest
from tramdata import *

TRAM_FILE = 'tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.all = tramdict

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_all_tram_lines_included(self):
        with open('tramlines.txt', 'r') as data:
            rows = csv.reader(data, delimiter = "\t")
            for line in rows:
                if line:
                    if line[0][0].isdigit():
                        self.assertIn(line[0].split(':')[0], self.linedict, msg=line[0][0] + ' not in linedict')

    def test_all_stops_in_line(self):
        with open('tramlines.txt', 'r') as data:
            rows = csv.reader(data, delimiter = "\t")
            for line in rows:
                if line:
                    if line[0][0].isdigit():
                        line_nr = line[0].split(':')[0]
                    else:
                        stop = line[0].rsplit(" ", 1)[0].rstrip()
                        self.assertIn(stop, self.linedict[line_nr], msg=stop + ' not in ' + line_nr)

    def test_all_distances_less_than_20_km(self):
        for stop1 in self.stopdict:
            for stop2 in self.stopdict:
                self.assertLess(distance_between_stops(self.stopdict, stop1, stop2), 20, msg='distance from ' +stop1+ 'to' +stop2+ ' greater than 20km')

    def test_if_time_from_a_to_b_same_as_time_from_b_to_a(self):
        for line in self.linedict:
            for i in range(len(self.linedict[line]) - 1):
                for y in range(i, len(self.linedict[line])):
                    self.assertEqual(time_between_stops(self.all, line, self.linedict[line][i], self.linedict[line][y]), time_between_stops(self.all, line, self.linedict[line][y], self.linedict[line][i]), msg = 'Reversed time not the same')

    def test_dialogue(self):
        for stop1 in self.stopdict:
            for stop2 in self.stopdict:
                self.assertEqual(answer_query(f'via {stop1}', 'lines passing stop'), lines_via_stop(self.linedict, stop1), msg='Not same output')
                self.assertEqual(answer_query(f'between {stop1} and {stop2}', 'lines between stops'), lines_between_stops(self.linedict, stop1, stop2), msg='Not same output')
                self.assertEqual(answer_query(f'distance from {stop1} to {stop2}', 'distance from a to b'), distance_between_stops(self.stopdict, stop1, stop2), msg='Not same output')

        for line in self.linedict:
            for stop1 in self.linedict[line]:
                for stop2 in self.linedict[line]:
                    self.assertEqual(answer_query(f'with {line} from {stop1} to {stop2}', 'time from a to b'),
                    time_between_stops(self.all, line, stop1, stop2), msg='Not same output')

if __name__ == '__main__':
    unittest.main()
