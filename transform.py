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
        curs.execute("ALTER USER[alpha] WITH DEFAULT_SCHEMA=[based]")
        curs.execute('SELECT name, botanist_id FROM botanist')
        rows = curs.fetchall()
        # logging.info('Created a mapping for "botanist" values')
    return {row["name"]: row["botanist_id"] for row in rows}


def get_plant_data(plant: dict) -> tuple:
    pass


def get_botanist_data(plant: dict, conn: pymssql.Connection) -> tuple:
    existing_botatnists = get_botanist_mapping(conn)
    try:
        id = existing_botatnists[plant['botanist']]
    except KeyError:
        try:
            id = max(existing_botatnists.values()) + 1
        except ValueError:
            id = 1


def get_origin_data(plant: dict) -> tuple:
    pass


def get_images_data(plant: dict) -> tuple:
    pass


def get_license_data(plant: dict) -> tuple:
    pass


def get_health_data(plant: dict) -> tuple:
    pass


def main(plants: list[dict]) -> dict[list[tuple]]:
    pass


if __name__ == "__main__":
    print(max({}))
