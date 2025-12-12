# src/tests/test_algorithms.py
import unittest
from game_logic import generate_distance_matrix, run_all
from game_logic import CITIES

class TestAlgorithms(unittest.TestCase):
    def test_small_run(self):
        # create deterministic small matrix for repeatability
        # override random matrix with a small known 4-city matrix
        mat = [
            [0,10,15,20,50,50,50,50,50,50],
            [10,0,35,25,50,50,50,50,50,50],
            [15,35,0,30,50,50,50,50,50,50],
            [20,25,30,0,50,50,50,50,50,50],
            [50,50,50,50,0,50,50,50,50,50],
            [50,50,50,50,50,0,50,50,50,50],
            [50,50,50,50,50,50,0,50,50,50],
            [50,50,50,50,50,50,50,0,50,50],
            [50,50,50,50,50,50,50,50,0,50],
            [50,50,50,50,50,50,50,50,50,0],
        ]
        home = "A"
        selected = ["B","C","D"]
        results = run_all(mat, home, selected)
        self.assertIn("Brute Force", results)
        self.assertIn("Nearest Neighbour", results)
        self.assertIn("Held-Karp", results)
        # distances should be positive
        for v in results.values():
            self.assertGreaterEqual(v["distance"], 0)

if __name__ == "__main__":
    unittest.main()
