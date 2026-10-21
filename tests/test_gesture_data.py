import csv
import math
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GESTURE_DATA_DIR = PROJECT_ROOT / "static" / "hand_gesture_data"


class GestureDataTests(unittest.TestCase):
    def test_trained_model_artifacts_are_present(self):
        self.assertGreater((PROJECT_ROOT / "gesture_model.pkl").stat().st_size, 0)
        self.assertGreater((PROJECT_ROOT / "gesture_map.pkl").stat().st_size, 0)

    def test_seeded_gesture_files_are_present(self):
        expected_files = {f"f{index}.csv" for index in range(1, 8)}
        actual_files = {path.name for path in GESTURE_DATA_DIR.glob("*.csv")}
        self.assertEqual(actual_files, expected_files)

    def test_each_gesture_row_has_63_finite_landmark_values(self):
        for path in sorted(GESTURE_DATA_DIR.glob("*.csv")):
            with self.subTest(file=path.name):
                with path.open(newline="", encoding="utf-8") as data_file:
                    rows = list(csv.reader(data_file))

                self.assertTrue(rows, f"{path.name} contains no samples")
                for row_number, row in enumerate(rows, start=1):
                    self.assertEqual(
                        len(row),
                        63,
                        f"{path.name}:{row_number} should contain 63 coordinates",
                    )
                    self.assertTrue(
                        all(math.isfinite(float(value)) for value in row),
                        f"{path.name}:{row_number} contains a non-finite value",
                    )


if __name__ == "__main__":
    unittest.main()
