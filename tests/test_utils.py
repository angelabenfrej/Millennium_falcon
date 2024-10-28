import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dev.utils import calculate_capture_probability, find_best_path

class TestUtils(unittest.TestCase):
    def test_calculate_capture_probability_one_encounter(self):
        self.assertAlmostEqual(calculate_capture_probability(1), 0.1, places=2)

    def test_calculate_capture_probability_multiple_encounters(self):
        self.assertAlmostEqual(calculate_capture_probability(2), 0.19, places=2)

    def test_calculate_capture_probability_three_encounters(self):
        self.assertAlmostEqual(calculate_capture_probability(3), 0.271, places=3)
    def test_find_best_path_no_bounty_hunters(self):
        routes = [
            {'origin': 'Tatooine', 'destination': 'Alderaan', 'travel_time': 4},
            {'origin': 'Alderaan', 'destination': 'Endor', 'travel_time': 3}
        ]
        countdown = 10
        bounty_hunters = []
        autonomy = 7  
        probability = find_best_path(routes, countdown, bounty_hunters, autonomy)
        self.assertEqual(probability, 100.0)

if __name__ == '__main__':
    unittest.main()
