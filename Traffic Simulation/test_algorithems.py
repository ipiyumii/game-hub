import unittest
from collections import defaultdict
from ford_fulkerson import create_ford_fulkerson
from edmonds_karp import create_edmonds_karp

class TestMaxFlowAlgorithms(unittest.TestCase):

    def setUp(self):
        self.ff = create_ford_fulkerson()
        self.ek = create_edmonds_karp()

    def test_simple_network(self):
        graph = {
            'A': {'B': 10, 'C': 5},
            'B': {'C': 15, 'D': 8},
            'C': {'D': 7},
            'D': {'T': 10},
            'T': {}
        }

        max_flow_ff, _ = self.ff.max_flow(graph, 'A', 'T')
        max_flow_ek, _ = self.ek.max_flow(graph, 'A', 'T')

        # Both algorithms should give same result
        self.assertEqual(max_flow_ff, max_flow_ek)
        self.assertEqual(max_flow_ff, 10)

    def test_no_path(self):
        graph = {
            'A': {'B': 10},
            'B': {},
            'T': {}
        }

        max_flow_ff, _ = self.ff.max_flow(graph, 'A', 'T')
        max_flow_ek, _ = self.ek.max_flow(graph, 'A', 'T')

        self.assertEqual(max_flow_ff, 0)
        self.assertEqual(max_flow_ek, 0)

    def test_single_path(self):
        graph = {
            'A': {'B': 5},
            'B': {'T': 3},
            'T': {}
        }

        max_flow_ff, _ = self.ff.max_flow(graph, 'A', 'T')
        max_flow_ek, _ = self.ek.max_flow(graph, 'A', 'T')

        self.assertEqual(max_flow_ff, 3)
        self.assertEqual(max_flow_ek, 3)

    def test_complex_network(self):
        """Test a more complex network"""
        graph = {
            'A': {'B': 16, 'C': 13},
            'B': {'C': 10, 'D': 12},
            'C': {'B': 4, 'E': 14},
            'D': {'C': 9, 'T': 20},
            'E': {'D': 7, 'T': 4},
            'T': {}
        }

        max_flow_ff, _ = self.ff.max_flow(graph, 'A', 'T')
        max_flow_ek, _ = self.ek.max_flow(graph, 'A', 'T')

        self.assertEqual(max_flow_ff, max_flow_ek)
        self.assertEqual(max_flow_ff, 23)

if __name__ == '__main__':
    unittest.main()