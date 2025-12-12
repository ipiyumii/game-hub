# test_game_logic.py
import unittest
import game_logic

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        # Sample distance matrix for 4 cities
        self.cities = ["A", "B", "C", "D"]
        self.dist_matrix = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]
        self.start_idx = 0  # "A"
        self.city_indices = [1, 2, 3]  # B, C, D

    def test_generate_distance_matrix(self):
        m = game_logic.generate_distance_matrix(50, 100)
        self.assertEqual(len(m), len(game_logic.CITIES))
        self.assertEqual(len(m[0]), len(game_logic.CITIES))
        # distances should be within range
        for i in range(len(m)):
            for j in range(len(m)):
                if i != j:
                    self.assertGreaterEqual(m[i][j], 50)
                    self.assertLessEqual(m[i][j], 100)

    def test_brute_force_tsp(self):
        route, cost, _ = game_logic.brute_force_tsp(self.dist_matrix, self.start_idx, self.city_indices)
        self.assertEqual(route[0], self.start_idx)
        self.assertEqual(route[-1], self.start_idx)
        self.assertEqual(len(route), len(self.city_indices) + 2)

    def test_nearest_neighbour_tsp(self):
        route, cost, _ = game_logic.nearest_neighbour_tsp(self.dist_matrix, self.start_idx, self.city_indices)
        self.assertEqual(route[0], self.start_idx)
        self.assertEqual(route[-1], self.start_idx)

    def test_held_karp_tsp(self):
        route, cost, _ = game_logic.held_karp_tsp(self.dist_matrix, self.start_idx, self.city_indices)
        self.assertEqual(route[0], self.start_idx)
        self.assertEqual(route[-1], self.start_idx)

    def test_tsp_recursive(self):
        route, cost, _ = game_logic.tsp_recursive(self.dist_matrix, self.start_idx, self.city_indices)
        self.assertEqual(route[0], self.start_idx)
        self.assertEqual(route[-1], self.start_idx)

    def test_run_all(self):
        selected_labels = ["B", "C", "D"]
        results = game_logic.run_all(self.dist_matrix, "A", selected_labels)
        self.assertIn("Brute Force", results)
        self.assertIn("Recursive TSP", results)
        self.assertIn("Nearest Neighbour", results)
        self.assertIn("Held-Karp (DP)", results)

if __name__ == "__main__":
    unittest.main()
