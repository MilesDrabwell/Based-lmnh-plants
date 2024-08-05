"""Python script to retrieve plant data from the API asynchronously"""

import asyncio
import aiohttp


URL = "https://data-eng-plants-api.herokuapp.com/plants/{}"
NUMBER_OF_PLANTS = 50


async def get_plant_data(plants: int = NUMBER_OF_PLANTS) -> list[dict]:
    """Asynchronous function to retrieve the plant data for multiple plants"""
    plant_ids = range(plants + 1)
    plants_data = []

    async with aiohttp.ClientSession() as session:

        tasks = [session.get(URL.format(plant_id), ssl=False) for plant_id in plant_ids]

        responses = await asyncio.gather(*tasks)
        for response in responses:
            plants_data.append(await response.json())
        return plants_data


if __name__ == "__main__":
    print(asyncio.run(get_plant_data()))
