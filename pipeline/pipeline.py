"""Python script to retrieve plant data from the API asynchronously"""

import time
import asyncio
from extract import get_api_plant_data, new_plant_ids
from transform import get_table_data, get_connection
from load import load
import logging
import requests

logger = logging.getLogger()


URL = "https://data-eng-plants-api.herokuapp.com/plants/{}"
PLANT_IDS = list(range(1, 51))

url = "https://data-eng-plants-api.herokuapp.com/plants/{}"


def get_plant_data_slow() -> list[dict]:

    plant_ids = range(1)
    results = []
    for plant_id in plant_ids:
        response = requests.get(url.format(plant_id))
        results.append(response.json())
    return results


async def main() -> None:
    """Main function to run the script in a while loop"""
    plant_ids = PLANT_IDS
    conn = get_connection()
    while True:
        start_time = time.time()
        logger.info("fetching plant data from api")
        plants_data = await get_api_plant_data(plant_ids)
        plant_ids = new_plant_ids(plants_data)
        logger.info("plant data acquired from api")
        logger.info("transforming plant data ready for upload")
        transformed = get_table_data(plants_data, conn)
        logger.info("transformed plant data uploading")
        load(conn, transformed)
        logger.info("all plant data uploaded")
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"API calls took {duration} seconds")
        if duration < 60:
            time.sleep(60 - duration)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("hellllllloooooo wooooorllllllddddddd")
    print(get_plant_data_slow())
    asyncio.run(main())
