import requests
import time


url = "https://data-eng-plants-api.herokuapp.com/plants/{}"


def get_plant_data() -> list[dict]:

    plant_ids = range(51)
    results = []
    for plant_id in plant_ids:
        response = requests.get(url.format(plant_id))
        results.append(response.json())
    return results


if __name__ == "__main__":
    start = time.time()
    print(get_plant_data())
    end = time.time()
    total_time = end - start
    print("It took {} seconds to make the API calls".format(total_time))
