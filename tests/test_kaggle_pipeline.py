import json
import tempfile
import unittest
from pathlib import Path

from scripts.kaggle_pipeline import _read_submission, prepare


class KagglePipelineTests(unittest.TestCase):
    def test_prepare_writes_public_offline_kernel_and_paper_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle = Path(temp) / "bundle"
            kernel_dir, paper_dir = prepare("Example_User", bundle)
            metadata = json.loads((kernel_dir / "kernel-metadata.json").read_text())
            self.assertEqual(metadata["id"], "Example_User/arc-agi-2-rulelab")
            self.assertEqual(metadata["is_private"], "false")
            self.assertEqual(metadata["enable_internet"], "false")
            self.assertEqual(metadata["competition_sources"], ["arc-prize-2026-arc-agi-2"])
            self.assertTrue((kernel_dir / metadata["code_file"]).is_file())
            self.assertTrue((paper_dir / "paper_track_writeup.md").is_file())
            self.assertTrue((paper_dir / "cover.png").is_file())
            self.assertIn("PUBLICATION_CHECKLIST.md", [p.name for p in bundle.iterdir()])

    def test_validator_accepts_exactly_two_valid_grids(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "submission.json"
            path.write_text(json.dumps({"task": [{
                "attempt_1": [[0, 1], [2, 3]],
                "attempt_2": [[3]],
            }]}))
            self.assertEqual(_read_submission(path)["task"][0]["attempt_1"], [[0, 1], [2, 3]])

    def test_validator_rejects_invalid_attempt_set_and_grid_values(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "submission.json"
            path.write_text(json.dumps({"task": [{"attempt_1": [[0]], "attempt_3": [[1]]}]}))
            with self.assertRaises(ValueError):
                _read_submission(path)
            path.write_text(json.dumps({"task": [{"attempt_1": [[10]], "attempt_2": [[0]]}]}))
            with self.assertRaises(ValueError):
                _read_submission(path)


if __name__ == "__main__":
    unittest.main()
