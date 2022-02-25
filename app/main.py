import logging
from datetime import datetime, timedelta
import os
import json
import subprocess
import gzip
import shutil
import logging
from typing import Dict
from google.cloud import storage


logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s")
logging.getLogger().setLevel(logging.INFO)


tables = [
    ("tc_positions", "servertime", "id"),
    ("tc_events", "eventtime", "positionid"),
]
path_prefix = "/tmp"


def archive(to_date: datetime):
    date_str = to_date.strftime("%Y%m%d")
    logging.info(f"Archive {date_str} started")

    dsn_config = _get_config("DSN_CONF")
    gcs_config = _get_config("GCS_CONF")

    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_config["bucket"])

    for table, time_field, pos_field in tables:
        dsn = [
            f"h={dsn_config['host']}",
            f"u={dsn_config['user']}",
            f"p={dsn_config['password']}",
            f"D={dsn_config['database']}",
            f"t={table}",
        ]
        filename = f"{dsn_config['database']}_{table}_{date_str}"
        infile = f"{path_prefix}/{filename}"
        clauses = [
            f'DATE({time_field}) < "{to_date.strftime("%Y-%m-%d")}"',
            f"{pos_field} NOT IN (SELECT positionid FROM tc_devices WHERE positionid IS NOT NULL)",
        ]
        command = _get_command(",".join(dsn), infile, " AND ".join(clauses))

        logging.info(f"Dumping {dsn_config['database']}.{table}")
        result = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(
                f"Return code: {result.returncode}, Error: {result.stderr.decode('utf-8')}"
            )

        if os.path.exists(infile):
            outfile = f"{path_prefix}/{filename}.gz"
            logging.info(f"Compressing {dsn_config['database']}.{table}")
            with open(infile, "rb") as fin:
                with gzip.open(outfile, "wb") as fout:
                    shutil.copyfileobj(fin, fout)

            blob = bucket.blob(f"{date_str}/{filename}.gz")
            logging.info(f"Uploading {dsn_config['database']}.{table}")
            blob.upload_from_filename(outfile)

    logging.info(f"Archive {date_str} completed")


def _get_command(dsn: str, file: str, where: str) -> str:
    return f"""
        pt-archiver \
            --source {dsn} \
            --where '{where}' \
            --file '{file}' \
            --header \
            --statistics \
            --why-quit \
            --limit 100 \
            --commit-each \
            --optimize s \
            --skip-foreign-key-checks \
            --no-check-charset
    """


def _get_config(key: str) -> Dict:
    conf_file = os.getenv(key)
    if not conf_file:
        raise Exception(f"Environment variable {key} not set")

    if not os.path.isfile(conf_file):
        raise Exception(f"File {conf_file} not found")

    with open(conf_file, "r") as f:
        config = json.load(f)

    return config


if __name__ == "__main__":
    days_past = int(os.getenv("DAYS_PAST", "180"))
    to_date = datetime.now() - timedelta(days=days_past)
    archive(to_date)
