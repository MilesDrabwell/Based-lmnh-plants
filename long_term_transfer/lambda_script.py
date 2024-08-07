"""Python script run on AWS Lambda to move data from short to long term storage every 24 hours"""

from os import getenv
from os.path import splitext
from csv import DictWriter
from datetime import datetime, timedelta
from pymssql import connect
from pymssql._pymssql import Connection
import boto3
from botocore import client
from dotenv import load_dotenv

FILENAME = "long_term_data.csv"
BUCKET_NAME = "c12-lmnh-alpha-storage"


def get_connection() -> Connection:
    """Establishing a connection to our RDS"""
    conn = connect(
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        database=getenv("DB_NAME"),
    )
    return conn


def calculate_cutoff_time() -> datetime:
    """Calculates the datetime object for 24 hours ago"""
    return datetime.today() - timedelta(days=1)


def get_old_data(conn: Connection, cutoff_time: datetime) -> list[dict]:
    """Executes SQL query to retrieve rows older than the cutoff time"""
    query = """SELECT * FROM alpha.plant_health WHERE recording_time <= %s"""
    with conn.cursor(as_dict=True) as cur:
        cur.execute(query, (cutoff_time,))
        rows = cur.fetchall()
    return rows


def delete_old_data(conn: Connection, cutoff_time: datetime) -> None:
    """Executes SQL query to delete rows older than the cutoff time"""
    query = """DELETE FROM alpha.plant_health WHERE recording_time <= %s"""
    with conn.cursor() as cur:
        cur.execute(query, (cutoff_time,))
    conn.commit()


def get_client() -> client:
    """Initiates a connection to the S3 AWS Cloud using required credentials."""
    aws_client = boto3.client(
        "s3",
        aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
    )
    return aws_client


def write_data_to_csv(
    aws_client: client, old_data: list[dict], cutoff_time: datetime
) -> None:
    """Retrieves existing long term data from S3 bucket and appends rows
    without loading entire file into memory and sends it back to the s3 bucket"""
    date_string = cutoff_time.strftime("%d-%m-%y")
    prefix, extension = splitext(FILENAME)[0]
    dated_filename = prefix + "_" + date_string + extension
    with open(dated_filename, "a", newline="", encoding="utf-8") as f:
        field_names = [
            "plant_health_id",
            "plant_id",
            "recording_time",
            "soil_moisture",
            "temperature",
            "last_watered",
        ]
        dict_writer = DictWriter(f, fieldnames=field_names)
        dict_writer.writeheader()
        dict_writer.writerows(old_data)
    aws_client.upload_file(dated_filename, BUCKET_NAME, dated_filename)


def handler(event: dict, context) -> dict:
    """Handler function called by AWS Lambda that moves data from short to long term storage"""
    conn = get_connection()
    cutoff_time = calculate_cutoff_time()
    old_data = get_old_data(conn, cutoff_time)
    row_count = len(old_data)
    if row_count:
        delete_old_data(conn, cutoff_time)
        aws_client = get_client()
        write_data_to_csv(aws_client, old_data, cutoff_time)
    return {"rows_transferred": row_count}


if __name__ == "__main__":
    load_dotenv()
    print(handler({}, None))
