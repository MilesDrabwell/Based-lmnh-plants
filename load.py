"""Python script that will load the transformed data to the RDS"""
from os import getenv
from pymssql import connect
# from transform import get_table_data

#get_Table_data is the main function that returns a dict of the format:
# {
#     'health data': [(1),(2),(1) ...],
#     'botanist data': [('Bob', '123@gmail.com'),('Rob',...),('Sandra') ...],
#     ...
# }
#(from https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16#best-practices)
# INSERT INTO Production.UnitMeasure  
# VALUES (N'FT2', N'Square Feet ', '20080923'), (N'Y', N'Yards', '20080923')
#     , (N'Y3', N'Cubic Yards', '20080923');  GO

#[{'plant':(3, 'super cool plant', 'sciency name', 4, 6, 7)}]


def get_connection():
    conn = connect(host=getenv("DB_HOST"),
                   port=getenv('DB_PORT'),
                   user=getenv('DB_USER'),
                   password=getenv('DB_PASSWORD'),
                   database=getenv("DB_NAME"))
    return conn

def insert_license(conn:pymssql.Connection, licence_data:list[tuple]):
    """Returns the query to add all the license information"""
    query = '''
        INSERT INTO license(license_id, license_name, license_url)
        VALUES (%s, %s, %s);
    '''
    with conn.cursor as cur:
        cur.executemany(query, licence_data)
    conn.commit()

def insert_images(conn:pymssql.Connection, images_data: list[tuple]):
    """Returns the query to add all the image information"""
    query = '''
        INSERT INTO images(image_id, license_id, thumbnail_url, small_url, medium_url, regular_url, original_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''
    with conn.cursor as cur:
        cur.executemany(query, images_data)
    conn.commit()

def insert_origin_location(conn:pymssql.Connection, location_data: list[tuple]):
    """Returns the query to add all the origin information"""
    query = '''
        INSERT INTO origin_location(latitude, longitude, locality_name, continent_name, city_name, country_name)
        VALUES (%s, %s, %s, %s, %s, %s);
    '''
    with conn.cursor as cur:
        cur.executemany(query, location_data)
    conn.commit()

def insert_botanist(conn:pymssql.Connection, botanist_data: list[tuple]):
    """Returns the query to add all the botanist information"""
    query = '''
        INSERT INTO botanist(botanist_id, name, email, phone)
        VALUES (%s, %s, %s, %s);
    '''
    with conn.cursor as cur:
        cur.executemany(query, botanist_data)
    conn.commit()

def insert_plant_health(conn:pymssql.Connection, health_data: list[tuple]):
    """Returns the query to add all the plant health information"""
    query = '''
        INSERT INTO plant_health(plant_id, recording_time, soil_moisture, temperature, last_watered)
        VALUES (%s, %s, %s, %s, %s);
    '''
    with conn.cursor as cur:
        cur.executemany(query, health_data)
    conn.commit()

def insert_plant(conn:pymssql.Connection, botanist_data: list[tuple]):
    """Returns the query to link and add all the plant data"""
    query = '''
        INSERT INTO plant(plant_id, plant_name, plant_scientific_name, botanist_id, image_id, origin_location_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    '''
    with conn.cursor as cur:
        cur.executemany(query, pl_data)
    conn.commit()


def load(all_plants: dict[list[tuple]], conn: pymssql.Connection):
    """adding all the data obtained to our RDS"""
    if all_plants.get('license'):
        insert_license(conn, all_plants['license'])
    if all_plants.get('images'):
        insert_images(conn, all_plants['images'])
    if all_plants.get('origin_location'):
        insert_origin_location(conn, all_plants['origin_location'])
    if all_plants.get('botanist'):
        insert_botanist(conn, all_plants['botanist'])
    if all_plants.get('plant_health'):
        insert_plant_health(conn, all_plants['plant_health'])
    if all_plants.get('plant'):
        insert_plant(conn, all_plants['plant'])
            
            
if __name__ == "__main__":
    connection = get_connection()
    clean_data = get_table_data(connection)
    load(clean_data, conn)