import csv
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from readings import ReadingLog


class ReadingLogTests(unittest.TestCase):
    def test_appends_with_one_header_and_preserves_barcode_text(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "nested" / "readings.csv"
            for value in ["001234", 'shelf,"A"']:
                log = ReadingLog(path)
                try:
                    log.write(value)
                finally:
                    log.close()
            with path.open(newline="", encoding="utf-8") as source:
                rows = list(csv.reader(source))
            self.assertEqual(rows[0], ["timestamp_utc", "barcode"])
            self.assertEqual([row[1] for row in rows[1:]], ["001234", 'shelf,"A"'])
            for row in rows[1:]:
                self.assertEqual(datetime.fromisoformat(row[0]).utcoffset(), timedelta(0))

    def test_rejects_unrelated_csv_without_changing_it(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "other.csv"
            path.write_text("name,quantity\nitem,2\n", encoding="utf-8")
            before = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "Unexpected CSV header"):
                ReadingLog(path)
            self.assertEqual(path.read_bytes(), before)
