import pymssql
from os import getenv
from datetime import datetime


def check_for_error(plant: dict) -> bool:
    if plant.get("error"):
        return False
    if not isinstance(plant, dict):
        return False
    if plant.get("plant_id") is None or not isinstance(plant.get("plant_id"), int):
        return False
    if plant.get("plant_id") < 0:
        return False
    return True


def get_connection() -> pymssql.Connection:
    return pymssql.connect(host=getenv("DB_HOST"),
                           user=getenv("DB_USER"),
                           password=getenv('DB_PASSWORD'),
                           database=getenv("DB_NAME"),
                           port=getenv("DB_PORT"))


def get_botanist_mapping(conn: pymssql.Connection) -> dict:
    with conn.cursor(as_dict=True) as curs:
        curs.execute('SELECT name, botanist_id FROM alpha.botanist')
        rows = curs.fetchall()
        # logging.info('Created a mapping for "botanist" values')
    return {row["name"]: row["botanist_id"] for row in rows}


def initial_botanist_mapping(plants: list[dict]) -> dict:
    id = 1
    mapping = {}
    for plant in plants:
        if not mapping.get(plant["botanist"]["name"]):
            mapping[plant["botanist"]["name"]] = id
            id += 1
    return mapping


def get_botanist_data(plant: dict, mapping: dict, initial_mapping: dict) -> tuple | None:
    if not plant.get("botanist"):
        return None
    if mapping:
        id = mapping.get(plant["botanist"]["name"])
        if id:
            return None
        id = max(mapping.values()) + 1
    else:
        id = initial_mapping.get(plant['botanist']["name"])
    return (id, plant.get("botanist").get("name"), plant.get("botanist").get("email"), plant.get("botanist").get("phone"))


def get_origin_mapping(conn: pymssql.Connection) -> dict:
    with conn.cursor(as_dict=True) as curs:
        curs.execute(
            'SELECT country_code, origin_location_id FROM alpha.origin_location')
        rows = curs.fetchall()
        # logging.info('Created a mapping for "origin" values')
    return {row["country_code"]: row["origin_location_id"] for row in rows}


def initial_origin_mapping(plants: list[dict]) -> dict:
    id = 1
    mapping = {}
    for plant in plants:
        if not mapping.get(plant["origin_location"][3]):
            mapping[plant["origin_location"][3]] = id
            id += 1
    return mapping


def get_origin_data(plant: dict, mapping: dict, initial_mapping: dict) -> tuple | None:
    if not plant.get("origin_location"):
        return None
    if mapping:
        id = mapping.get(plant['origin_location'][3])
        if id:
            return None
        id = max(mapping.values()) + 1
    else:
        id = initial_mapping.get(plant['origin_location'][3])
    continent = plant.get('origin_location')[4].split("/")[0]
    city = plant.get('origin_location')[4].split("/")[1]
    return (id, float(plant.get('origin_location')[0]), float(plant.get('origin_location')[1]), plant.get('origin_location')[2], continent, city, plant.get('origin_location')[3])


def get_license_mapping(conn: pymssql.Connection) -> dict:
    with conn.cursor(as_dict=True) as curs:
        curs.execute(
            'SELECT license_name, license_id FROM alpha.license')
        rows = curs.fetchall()
        # logging.info('Created a mapping for "license" values')
    return {row["license_name"]: row["license_id"] for row in rows}


def initial_license_mapping(plants: list[dict]) -> dict:
    id = 1
    mapping = {}
    for plant in plants:
        if not plant.get("images"):
            continue
        if not mapping.get(plant["images"]["license_name"]):
            mapping[plant["images"]["license_name"]] = id
            id += 1
    return mapping


def get_license_data(plant: dict, mapping: dict, initial_mapping: dict) -> tuple | None:
    if not plant.get("images"):
        return None
    if mapping:
        id = mapping.get(plant["images"]["license_name"])
        if id:
            return None
        id = max(mapping.values()) + 1
    else:
        id = initial_mapping.get(plant["images"]["license_name"])
    return (id, plant.get("images").get("license_name"), plant.get("images").get("license_url"))


def get_images_mapping(conn: pymssql.Connection) -> dict:
    with conn.cursor(as_dict=True) as curs:
        curs.execute(
            'SELECT regular_url, image_id FROM alpha.images')
        rows = curs.fetchall()
        # logging.info('Created a mapping for "license" values')
    return {row["regular_url"]: row["image_id"] for row in rows}


def initial_images_mapping(plants: list[dict]) -> dict:
    id = 1
    mapping = {}
    for plant in plants:
        if not plant.get("images"):
            continue
        if not mapping.get(plant["images"]["regular_url"]):
            mapping[plant["images"]["regular_url"]] = id
            id += 1
    return mapping


def get_images_data(plant: dict, mapping: dict, initial_mapping: dict, license_mapping: dict, initial_license_mapping: dict) -> tuple | None:
    if not plant.get("images"):
        return None
    if mapping:
        id = mapping.get(plant["images"]["regular_url"])
        if id:
            return None
        id = max(mapping.values()) + 1
    else:
        id = initial_mapping.get(plant["images"]["regular_url"])
    license_id = license_mapping.get(plant["images"]["license_name"])
    if not license_id:
        license_id = initial_license_mapping.get(
            plant["images"]["license_name"])
    return (id, license_id, plant.get("images").get("thumbnail_url"), plant.get("images").get("small_url"), plant.get("images").get("medium_url"), plant.get("images").get("regular_url", plant.get("images").get("original_url")))


def get_plant_mapping(conn: pymssql.Connection) -> dict:
    with conn.cursor(as_dict=True) as curs:
        curs.execute(
            'SELECT * FROM alpha.plant')
        rows = curs.fetchall()
        # logging.info('Created a mapping for "license" values')
    return {row["plant_name"]: row["plant_id"] for row in rows}


def get_plant_data(plant: dict, mapping: dict, origin_mapping: dict, initial_origin_mapping: dict, botanist_mapping: dict, initial_botanist_mapping: dict, image_mapping: dict, initial_image_mapping: dict) -> tuple | None:
    if not plant.get("name"):
        return None
    id = plant.get("plant_id")
    if id in mapping.values():
        return None
    if plant.get("origin_location"):
        origin_location_id = origin_mapping.get(plant["origin_location"][3])
        if not origin_location_id:
            origin_location_id = initial_origin_mapping.get(
                plant["origin_location"][3])
    else:
        origin_location_id = None
    if plant.get("botanist"):
        botanist_id = botanist_mapping.get(plant['botanist']["name"])
        if not botanist_id:
            botanist_id = initial_botanist_mapping.get(
                plant['botanist']["name"])
    else:
        botanist_id = None
    if plant.get("images"):
        image_id = image_mapping.get(plant["images"]["regular_url"])
        if not image_id:
            image_id = initial_image_mapping.get(
                plant["images"]["regular_url"])
    else:
        image_id = None
    return (id, plant.get("name"), plant.get("scientific_name")[0], botanist_id, image_id, origin_location_id)


def get_health_data(plant: dict) -> tuple:
    try:
        recording_time = datetime.strptime(
            plant.get('recording_taken'), "%Y-%m-%d %H:%M:%S")
    except:
        recording_time = None
    soil_moisture = float(plant.get("soil_moisture"))
    temperature = float(plant.get("temperature"))
    try:
        last_watered = datetime.strptime(
            plant.get("last_watered"), "%a, %d %b %Y %H:%M:%S %Z")
    except:
        last_watered = None
    return (plant.get("plant_id"), recording_time, soil_moisture, temperature, last_watered)


def get_table_data(plants: list[dict], conn: pymssql.Connection) -> dict[list[tuple]]:
    pass


if __name__ == "__main__":
    pass
