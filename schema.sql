--Script to delete foreign key constraints to drop tables.
DECLARE @sql NVARCHAR(MAX);

SELECT @sql = STRING_AGG('ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) + ' DROP CONSTRAINT ' + QUOTENAME(f.name) + ';', CHAR(13))
FROM sys.foreign_keys AS f
INNER JOIN sys.tables AS t ON f.parent_object_id = t.object_id
INNER JOIN sys.schemas AS s ON t.schema_id = s.schema_id
WHERE s.name = 'alpha';

IF @sql IS NOT NULL
BEGIN
    EXEC sp_executesql @sql;
END

IF OBJECT_ID('alpha.license', 'U') IS NOT NULL DROP TABLE alpha.license;
IF OBJECT_ID('alpha.origin_location', 'U') IS NOT NULL DROP TABLE alpha.origin_location;
IF OBJECT_ID('alpha.plant_health', 'U') IS NOT NULL DROP TABLE alpha.plant_health;
IF OBJECT_ID('alpha.images', 'U') IS NOT NULL DROP TABLE alpha.images;
IF OBJECT_ID('alpha.botanist', 'U') IS NOT NULL DROP TABLE alpha.botanist;
IF OBJECT_ID('alpha.plant', 'U') IS NOT NULL DROP TABLE alpha.plant;

--Begin creating the tables.
CREATE TABLE alpha.botanist(
    botanist_id INT NOT NULL PRIMARY KEY,
    name VARCHAR(MAX),
    email VARCHAR(MAX),
    phone VARCHAR(MAX)
);

CREATE TABLE alpha.origin_location(
    origin_location_id INT NOT NULL PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    locality_name VARCHAR(MAX),
    continent_name VARCHAR(MAX),
    city_name VARCHAR(MAX),
    country_code VARCHAR(MAX)
);

CREATE TABLE alpha.license(
    license_id INT NOT NULL PRIMARY KEY,
    license_name VARCHAR(MAX),
    license_url VARCHAR(MAX)
);

CREATE TABLE alpha.images(
    image_id INT NOT NULL PRIMARY KEY,
    license_id INT,
    thumbnail_url VARCHAR(MAX),
    small_url VARCHAR(MAX),
    medium_url VARCHAR(MAX),
    regular_url VARCHAR(MAX),
    original_url VARCHAR(MAX),
    FOREIGN KEY (license_id) REFERENCES alpha.license (license_id)
);

CREATE TABLE alpha.plant(
    plant_id INT NOT NULL PRIMARY KEY,
    plant_name VARCHAR(MAX),
    plant_scientific_name VARCHAR(MAX),
    botanist_id INT,
    image_id INT,
    origin_location_id INT,
    FOREIGN KEY (botanist_id) REFERENCES alpha.botanist (botanist_id),
    FOREIGN KEY (image_id) REFERENCES alpha.images (image_id),
    FOREIGN KEY (origin_location_id) REFERENCES alpha.origin_location (origin_location_id)
);

CREATE TABLE alpha.plant_health(
    plant_health_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    plant_id INT,
    recording_time DATETIME,
    soil_moisture FLOAT,
    temperature FLOAT,
    last_watered DATETIME,
    FOREIGN KEY (plant_id) REFERENCES alpha.plant (plant_id)
);