import pymssql
from os import environ
from dotenv import load_dotenv


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
    return pymssql.connect(host=environ["DB_HOST"],
                           user=environ["DB_USER"],
                           password=environ['DB_PASSWORD'],
                           database=environ["DB_NAME"],
                           port=environ["DB_PORT"])


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
    if mapping:
        id = mapping.get(plant["name"])
        if id:
            return None
        id = max(mapping.values()) + 1
    else:
        id = initial_mapping.get(plant['botanist']["name"])
    return (id, plant.get("name"), plant.get("email"), plant.get("phone"))


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
        if not mapping.get(plant["origin_location"]["country_code"]):
            mapping[plant["origin_location"]["country_code"]] = id
            id += 1
    return mapping


def get_origin_data(plant: dict, mapping: dict, initial_mapping: dict) -> tuple | None:
    if mapping:
        id = mapping.get(plant['country_code'])
        if id:
            return None
        id = max(mapping.values()) + 1
    else:
        id = initial_mapping.get(plant['botanist']["name"])
    return (id, plant.get("name"), plant.get("email"), plant.get("phone"))


def get_images_data(plant: dict) -> tuple:
    pass


def get_license_data(plant: dict) -> tuple:
    pass


def get_plant_data(plant: dict) -> tuple:
    pass


def get_health_data(plant: dict) -> tuple:
    pass


def get_table_data(plants: list[dict]) -> dict[list[tuple]]:
    pass


if __name__ == "__main__":
    print(max({}))
