import unittest
from trams import *

class TestTramData(unittest.TestCase):

    def setUp(self):
        self.network = readTramnetwork(TRAM_FILE)

    def test_transition_time_same_as_reverse(self):
        for stop1 in self.network.all_stops():
            for stop2 in self.network.all_stops():
                self.assertEqual(self.network.transition_time(stop1, stop2), self.network.transition_time(stop2, stop1),
                                 msg = 'Transition time not the same')

    def test_connectedness(self):
        for stop in self.network.all_stops():
            self.assertIsNotNone(self.network.neighbours(stop), msg = f'{stop} has no neighbours')


if __name__ == '__main__':
    unittest.main()
