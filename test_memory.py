
import unittest

from first_fit import first_fit
from best_fit import best_fit
from worst_fit import worst_fit
from metrics import calculate_metrics


class TestMemoryManagement(unittest.TestCase):

    def setUp(self):
        self.algorithms = {
            "First Fit": first_fit,
            "Best Fit": best_fit,
            "Worst Fit": worst_fit
        }

    # TEST 1: Normal memory allocation
    def test_normal_allocation(self):
        blocks = [100, 500, 200, 300]
        processes = [180, 250, 100]

        expected = {
            "First Fit": ([1, 1, 0], [0, 70, 200, 300]),
            "Best Fit": ([2, 3, 0], [0, 500, 20, 50]),
            "Worst Fit": ([1, 1, 2], [100, 70, 100, 300])
        }

        for name, algorithm in self.algorithms.items():
            with self.subTest(algorithm=name):
                allocation, remaining = algorithm(blocks, processes)

                self.assertEqual(allocation, expected[name][0])
                self.assertEqual(remaining, expected[name][1])

    # TEST 2: Insufficient memory
    def test_insufficient_memory(self):
        blocks = [100, 200]
        processes = [200, 201]

        for name, algorithm in self.algorithms.items():
            with self.subTest(algorithm=name):
                allocation, remaining = algorithm(blocks, processes)

                self.assertEqual(allocation, [1, -1])
                self.assertEqual(remaining, [100, 0])

                stats = calculate_metrics(
                    blocks, processes, allocation, remaining
                )

                self.assertEqual(stats["allocated"], 1)
                self.assertEqual(stats["failed"], 1)
                self.assertEqual(stats["used"], 200)
                self.assertEqual(stats["total_free"], 100)
                self.assertEqual(stats["largest_free"], 100)
                self.assertAlmostEqual(
                    stats["utilization"], 66.67, places=1
                )
                self.assertEqual(
                    stats["fragmentation_indicator"], 0.0
                )

    # TEST 3: External fragmentation
    def test_fragmentation(self):
        blocks = [100, 100]
        processes = [150]

        for name, algorithm in self.algorithms.items():
            with self.subTest(algorithm=name):
                allocation, remaining = algorithm(blocks, processes)

                self.assertEqual(allocation, [-1])
                self.assertEqual(remaining, [100, 100])

                stats = calculate_metrics(
                    blocks, processes, allocation, remaining
                )

                self.assertEqual(stats["allocated"], 0)
                self.assertEqual(stats["failed"], 1)
                self.assertEqual(stats["used"], 0)
                self.assertEqual(stats["total_free"], 200)
                self.assertEqual(stats["largest_free"], 100)
                self.assertEqual(stats["utilization"], 0.0)
                self.assertEqual(
                    stats["fragmentation_indicator"], 50.0
                )

    # TEST 4: Empty memory
    def test_empty_memory(self):
        blocks = []
        processes = [100, 200]

        for name, algorithm in self.algorithms.items():
            with self.subTest(algorithm=name):
                allocation, remaining = algorithm(blocks, processes)

                self.assertEqual(allocation, [-1, -1])
                self.assertEqual(remaining, [])

                stats = calculate_metrics(
                    blocks, processes, allocation, remaining
                )

                self.assertEqual(stats["allocated"], 0)
                self.assertEqual(stats["failed"], 2)
                self.assertEqual(stats["used"], 0)
                self.assertEqual(stats["total_free"], 0)
                self.assertEqual(stats["largest_free"], 0)
                self.assertEqual(stats["utilization"], 0.0)
                self.assertEqual(
                    stats["fragmentation_indicator"], 0.0
                )

    # TEST 5: Original memory blocks remain unchanged
    def test_original_blocks_unchanged(self):
        blocks = [100, 500, 200, 300]
        processes = [180, 250, 100]

        original_blocks = blocks.copy()

        for name, algorithm in self.algorithms.items():
            with self.subTest(algorithm=name):
                algorithm(blocks, processes)

                self.assertEqual(blocks, original_blocks)


if __name__ == "__main__":
    unittest.main(verbosity=2)
