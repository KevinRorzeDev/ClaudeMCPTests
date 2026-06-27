import datetime
import sys
import uuid

part_number = sys.argv[1] if len(sys.argv) > 1 else "UNKNOWN"
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
unique_id = uuid.uuid4().hex[:8].upper()
print(f"v0.2.0 — {timestamp}-{unique_id}-{part_number}")
