import unittest

from solver import Program, _programs_for_task, kaggle_payload, predict_task


class SolverTests(unittest.TestCase):
    def test_rotations_and_transpose(self):
        grid = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(Program("rot90").apply(grid), [[4, 1], [5, 2], [6, 3]])
        self.assertEqual(Program("rot180").apply(grid), [[6, 5, 4], [3, 2, 1]])
        self.assertEqual(Program("rot270").apply(grid), [[3, 6], [2, 5], [1, 4]])
        self.assertEqual(Program("transpose").apply(grid), [[1, 4], [2, 5], [3, 6]])

    def test_learns_geometry_and_consistent_color_map(self):
        task = {"train": [
            {"input": [[1, 2], [3, 4]], "output": [[4, 3], [2, 1]]},
            {"input": [[5, 6], [7, 8]], "output": [[8, 7], [6, 5]]},
        ], "test": [{"input": [[9, 0], [1, 2]]}]}
        programs = _programs_for_task(task)
        self.assertTrue(any(p.apply(e["input"]) == e["output"]
                            for p in programs for e in task["train"]))
        self.assertEqual(predict_task(task)[0][0], [[2, 1], [0, 9]])

    def test_crop_and_recolor(self):
        task = {"train": [
            {"input": [[0, 0, 0], [0, 1, 0], [0, 0, 0]], "output": [[2]]},
            {"input": [[0, 0, 0], [0, 3, 0], [0, 0, 0]], "output": [[4]]},
        ], "test": [{"input": [[0, 0, 0], [0, 5, 0], [0, 0, 0]]}]}
        self.assertIn(5, sum(predict_task(task)[0][0], []))
        guesses = predict_task(task)[0]
        self.assertIn([[5]], guesses)

    def test_output_has_two_attempts_for_each_test_input(self):
        tasks = {"task_x": {"train": [], "test": [{"input": [[1, 0]]}, {"input": [[0, 1]]}]}}
        payload = kaggle_payload(tasks)
        self.assertEqual(len(payload["task_x"]), 2)
        for item in payload["task_x"]:
            self.assertEqual(set(item), {"attempt_1", "attempt_2"})
            self.assertIsInstance(item["attempt_1"], list)
            self.assertIsInstance(item["attempt_2"], list)


if __name__ == "__main__":
    unittest.main()
