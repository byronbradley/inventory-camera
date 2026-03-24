import csv
from datetime import datetime, timezone
from pathlib import Path


class ReadingLog:
    def __init__(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.file = path.open("a+", newline="", encoding="utf-8")
        try:
            self.file.seek(0)
            header = next(csv.reader(self.file), None)
            if header is not None and header != ["timestamp_utc", "barcode"]:
                raise ValueError(f"Unexpected CSV header in {path}")
            self.file.seek(0, 2)
            self.writer = csv.writer(self.file)
            if header is None:
                self.writer.writerow(["timestamp_utc", "barcode"])
                self.file.flush()
        except BaseException:
            self.file.close()
            raise

    def write(self, barcode):
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        self.writer.writerow([timestamp, barcode])
        self.file.flush()

    def close(self):
        self.file.close()
