import datetime
import uuid

timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
unique_id = uuid.uuid4().hex[:8].upper()
print(f"{timestamp}-{unique_id}")
