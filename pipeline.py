"""Python script to retrieve plant data from the API asynchronously"""

import time
import asyncio
from extract import get_api_plant_data, new_plant_ids
from transform import get_table_data, get_connection
from load import load

URL = "https://data-eng-plants-api.herokuapp.com/plants/{}"
PLANT_IDS = list(range(51))


async def main() -> None:
    """Main function to run the script in a while loop"""
    plant_ids = PLANT_IDS
    conn = get_connection()
    while True:
        start_time = time.time()
        plants_data = await get_api_plant_data(plant_ids)
        plant_ids = new_plant_ids(plants_data)
        transformed = get_table_data(plants_data, conn)
        load(conn, transformed)
        end_time = time.time()
        duration = end_time - start_time
        print(f"API calls took {duration} seconds")
        if duration < 60:
            time.sleep(60 - duration)


if __name__ == "__main__":
    asyncio.run(main())
