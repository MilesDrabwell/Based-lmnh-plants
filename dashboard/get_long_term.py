from os import getenv
from os.path import isfile
from boto3 import client
import pandas as pd

BUCKET_NAME = "c12-lmnh-based-storage"
BUCKET_KEY_NAME = 'Contents'


def get_client():
    """Initiates a connection to the S3 AWS Cloud using required credentials."""
    aws_client = client(
        "s3",
        aws_access_key_id=getenv("ACCESS_KEY_ID"),
        aws_secret_access_key=getenv("SECRET_ACCESS_KEY"),
    )
    return aws_client


def get_file_names(client: client, bucket_name: str) -> list[str]:
    """Gets the list of valid parquet filenames and downloads files not yet downloaded."""
    filenames = []
    objects = client.list_objects_v2(Bucket=bucket_name)

    for obj in objects[BUCKET_KEY_NAME]:
        filename = obj["Key"]
        if "long_term_data" in filename:
            filenames.append(filename)
            if not isfile(filename):
                get_client().download_file(BUCKET_NAME, filename, filename)

    return filenames


def combine_transaction_data_files(filenames: list[str]) -> pd.DataFrame:
    """Converts parquet files to a single pandas dataframe."""
    df = pd.DataFrame()
    for filename in filenames:
        parquet = pd.read_parquet(filename)
        df = pd.concat([df, parquet], ignore_index=True)
    return df


def get_long_term_data() -> pd.DataFrame:
    """
    Gets files from our based s3 bucket
    """
    client = get_client()
    filenames = get_file_names(client, BUCKET_NAME)
    return combine_transaction_data_files(filenames)


if __name__ == "__main__":
    get_long_term_data()
