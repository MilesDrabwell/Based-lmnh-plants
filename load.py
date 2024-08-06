"""Python script that will load the transformed data to the RDS"""
from os import getenv
from pymssql import connect, executemany
# from transform import get_table_data

#get_Table_data is the main function that returns a dict of the format:
# {
#     'health data': [(1),(2),(1) ...],
#     'botanist data': [('Bob', '123@gmail.com'),('Rob',...),('Sandra') ...],
#     ...
# }

#[{'plant':(3, 'super cool plant', 'sciency name', 4, 6, 7)}]


def get_connection():
    conn = connect(host=getenv("DB_HOST"),
                   port=getenv('DB_PORT'),
                   user=getenv('DB_USER'),
                   password=getenv('DB_PASSWORD'),
                   database=getenv("DB_NAME"))
    return conn

def insert_license() -> str:
    """Returns the query to add all the license information"""
    query = '''
        INSERT INTO license(license_id, license_name, license_url)
        VALUES %s;
    '''
    return query
    #(from https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16#best-practices)
    # INSERT INTO Production.UnitMeasure  
    # VALUES (N'FT2', N'Square Feet ', '20080923'), (N'Y', N'Yards', '20080923')
    #     , (N'Y3', N'Cubic Yards', '20080923');  GO

def insert_images() -> str:
    """Returns the query to add all the image information"""
    query = '''
        INSERT INTO images(image_id, license_id, thumbnail_url, small_url, medium_url, regular_url, original_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''
    return query

def insert_origin_location():
    """Returns the query to add all the origin information"""
    query = '''
        INSERT INTO origin_location(latitude, longitude, locality_name, continent_name, city_name, country_name)
        VALUES (%s, %s, %s, %s, %s, %s);
    '''
    return query

def insert_botanist():
    """Returns the query to add all the botanist information"""
    query = '''
        INSERT INTO botanist(botanist_id, name, email, phone)
        VALUES (%s, %s, %s, %s);
    '''
    return query

def insert_plant_health():
    """Returns the query to add all the plant health information"""
    query = '''
        INSERT INTO plant_health(plant_id, recording_time, soil_moisture, temperature, last_watered)
        VALUES (%s, %s, %s, %s, %s);
    '''
    return query

def insert_plant():
    """Returns the query to link and add all the plant data"""
    query = '''
        INSERT INTO plant(plant_id, plant_name, plant_scientific_name, botanist_id, image_id, origin_location_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    '''
    return query


def load(all_plants: dict[list[tuple]], connection: pymssql.Connection):
    """adding all the data obtained to our RDS"""
    with connection.cursor() as cur:
        if all_plants.get('license'):
            cur.execute(cur, insert_license(), all_plants['license'])
        if all_plants.get('images'):
            cur.execute(cur, insert_images(),  all_plants['images'])
        if all_plants.get('origin_location'):
            cur.execute(cur, insert_origin_location(),  all_plants['origin_location'])
        if all_plants.get('botanist'):
            cur.execute(cur, insert_botanist(),  all_plants['botanist'])
        if all_plants.get('plant_health'):
            cur.execute(cur, insert_plant_health(),  all_plants['plant_health'])
        if all_plants.get('plant'):
            cur.execute(cur, insert_plant(),  all_plants['plant'])
        cur.commit()
            
            
if __name__ == "__main__":
    conn = get_connection()
    clean_data = get_table_data(conn)
    load(clean_data, conn)