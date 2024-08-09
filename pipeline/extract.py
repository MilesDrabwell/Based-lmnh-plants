"""Python script to retrieve plant data from the API asynchronously"""

import asyncio
import aiohttp

INITIAL_NUMBER_OF_PLANTS = 51
URL = "https://data-eng-plants-api.herokuapp.com/plants/{}"
PLANT_IDS = list(range(INITIAL_NUMBER_OF_PLANTS))


async def get_api_plant_data(plant_ids: list) -> list[dict]:
    """Asynchronous function to retrieve the plant data for multiple plants"""
    if not isinstance(plant_ids, list):
        raise TypeError
    plants_data = []
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(URL.format(plant_id), ssl=False)
                 for plant_id in plant_ids]
        responses = await asyncio.gather(*tasks)

        for response in responses:
            plant_data = await response.json(content_type=None)
            plants_data.append(plant_data)
    return plants_data


def new_plant_ids(plants_data: list[dict]) -> list[int]:
    """Function to generate plant IDs for the next iteration"""
    plant_ids = []
    for plant_data in plants_data:
        if plant_data.get("error") != "plant not found":
            plant_ids.append(plant_data.get("plant_id"))

    next_plant_id = plant_ids[-1] + 1
    plant_ids.append(next_plant_id)
    return plant_ids
