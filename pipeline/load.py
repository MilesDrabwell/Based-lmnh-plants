"""Python script that will load the transformed data to the RDS"""

from os import getenv
import asyncio
from pymssql import connect
from pymssql._pymssql import Connection
from extract import get_api_plant_data
from transform import get_table_data

INITIAL_NUMBER_OF_PLANTS = 51

def get_connection() -> Connection:
    """Establishing a connection to our RDS"""
    conn = connect(
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        database=getenv("DB_NAME"),
    )
    return conn


def insert_license(conn: Connection, license_data: list[tuple]):
    """Returns the query to add all the license information"""
    query = """
        INSERT INTO license(license_id, license_name, license_url)
        VALUES (%s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.executemany(query, license_data)
    conn.commit()


def insert_images(conn: Connection, images_data: list[tuple]):
    """Returns the query to add all the image information"""
    query = """
        INSERT INTO images(image_id, license_id, thumbnail_url, small_url, medium_url, regular_url, original_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.executemany(query, images_data)
    conn.commit()


def insert_origin_location(conn: Connection, location_data: list[tuple]):
    """Returns the query to add all the origin information"""
    query = """
        INSERT INTO origin_location(origin_location_id, latitude, longitude, locality_name, continent_name, city_name, country_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.executemany(query, location_data)
    conn.commit()


def insert_botanist(conn: Connection, botanist_data: list[tuple]):
    """Returns the query to add all the botanist information"""
    query = """
        INSERT INTO botanist(botanist_id, name, email, phone)
        VALUES (%s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.executemany(query, botanist_data)
    conn.commit()


def insert_plant_health(conn: Connection, health_data: list[tuple]):
    """Returns the query to add all the plant health information"""
    query = """
        INSERT INTO plant_health(plant_id, recording_time, soil_moisture, temperature, last_watered)
        VALUES (%s, %s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.executemany(query, health_data)
    conn.commit()


def insert_plant(conn: Connection, plant_data: list[tuple]):
    """Returns the query to link and add all the plant data"""
    query = """
        INSERT INTO plant(plant_id, plant_name, plant_scientific_name, botanist_id, image_id, origin_location_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.executemany(query, plant_data)
    conn.commit()


def load(
    conn: Connection,
    all_plants: dict[list[tuple]],
) -> None:
    """Adding all the data obtained to our RDS"""
    if all_plants.get("license"):
        insert_license(conn, all_plants["license"])
    if all_plants.get("images"):
        insert_images(conn, all_plants["images"])
    if all_plants.get("origin_location"):
        insert_origin_location(conn, all_plants["origin_location"])
    if all_plants.get("botanist"):
        insert_botanist(conn, all_plants["botanist"])
    if all_plants.get("plant"):
        insert_plant(conn, all_plants["plant"])
    if all_plants.get("plant_health"):
        insert_plant_health(conn, all_plants["plant_health"])



