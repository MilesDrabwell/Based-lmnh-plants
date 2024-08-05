import asyncio
import aiohttp
import time


url = "https://data-eng-plants-api.herokuapp.com/plants/{}"


async def get_plant_data() -> list[dict]:
    plant_ids = range(51)
    results = []

    async with aiohttp.ClientSession() as session:

        tasks = [session.get(url.format(plant_id), ssl=False) for plant_id in plant_ids]

        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
        return results


if __name__ == "__main__":
    start = time.time()
    print(asyncio.run(get_plant_data()))
    end = time.time()
    total_time = end - start
    print("It took {} seconds to make the API calls".format(total_time))
