import logging
import os
from datetime import datetime, timedelta

from archive import archive

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s")
logging.getLogger().setLevel(logging.INFO)


if __name__ == "__main__":
    days_past = int(os.getenv("DAYS_PAST", "180"))
    to_date = datetime.now() - timedelta(days=days_past)
    archive(to_date)
