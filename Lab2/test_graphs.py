import unittest
from trams import *
from graphs import *

class TestTramData(unittest.TestCase):

    def setUp(self):
        self.network = readTramnetwork(TRAM_FILE)

    def test_all_edge_nodes_in_vertices(self):
        for edge in self.network.edges():
            self.assertIn(edge[0] and edge[1], self.network.vertices(), msg= f"{edge[0]} or {edge[1]} not in vertice list")

    def test_if_a_neighbouring_b_b_neighbouring_a(self):
        for stop1 in self.network.vertices():
            for stop2 in self.network.vertices():
                if stop1 in self.network.neighbours(stop2):
                    self.assertIn(stop2, self.network.neighbours(stop1), msg = f'{stop2} is not a neighbour to {stop1}' )

    def test_reversed_dijkstra(self):
        for stop1 in self.network.all_stops():
            for stop2 in self.network.all_stops():
                a_to_b = dijkstra(self.network, stop1, stop2, self.network.transition_time)['dist']
                b_to_a = dijkstra(self.network, stop2, stop1, self.network.transition_time)['dist']

                self.assertEqual(a_to_b, b_to_a, msg=f'Transition time not the same for {stop1._name} and {stop2._name} as reversed')

    def test_removing_edge_does_not_remove_vertex(self):
        for stop in self.network.all_stops():
            if stop._name == 'Chalmers':
                testing_stop1 = stop
            if stop._name == 'Korsvägen':
                testing_stop2 = stop
        self.network.remove_edge(testing_stop1, testing_stop2)

        self.assertIn(testing_stop1 and testing_stop2, self.network.vertices(), msg=f'{testing_stop2} or {testing_stop1} not in list of vertices')

    def test_removing_vertex_also_removes_edges(self):
        for stop in self.network.all_stops():
            if stop._name == 'Chalmers':
                testing_stop = stop
        self.network.remove_vertex(testing_stop)
        self.assertNotIn(testing_stop, self.network.edges(), msg=f'Removing {testing_stop} did not remove all edges')




if __name__ == '__main__':
    unittest.main()
