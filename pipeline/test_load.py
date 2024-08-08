# pylint: skip-file
"""Unit tests for the load.py script"""
import pytest
from unittest.mock import patch, MagicMock
from load import insert_license, insert_images, insert_origin_location, insert_botanist, insert_plant_health, insert_plant, load


@pytest.fixture
def fake_conn():
    return MagicMock()


@pytest.fixture
def fake_cur():
    return MagicMock()


class TestInsertLicense:
    def test_insert_license_execute_called_once(self, fake_conn, fake_cur):

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        result = insert_license(fake_conn, [(23, "license")])

        assert fake_cur.executemany.call_count == 1


class TestInsertImages:
    def test_insert_images_execute_called_once(self, fake_conn, fake_cur):

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        result = insert_images(fake_conn, [(23, "license")])

        assert fake_cur.executemany.call_count == 1


class TestInsertOriginLocation:
    def test_insert_origin_location_execute_called_once(self, fake_conn, fake_cur):

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        result = insert_origin_location(fake_conn, [(23, "license")])

        assert fake_cur.executemany.call_count == 1


class TestInsertBotanist:
    def test_insert_botanist_execute_called_once(self, fake_conn, fake_cur):

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        result = insert_botanist(fake_conn, [(23, "license")])

        assert fake_cur.executemany.call_count == 1


class TestInsertPlantHealth:
    def test_insert_plant_health_execute_called_once(self, fake_conn, fake_cur):

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        result = insert_plant_health(fake_conn, [(23, "license")])

        assert fake_cur.executemany.call_count == 1


class TestInsertPlant:
    def test_insert_plant_execute_called_once(self, fake_conn, fake_cur):

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        result = insert_plant(fake_conn, [(23, "license")])

        assert fake_cur.executemany.call_count == 1


class TestLoad:
    def test_load_insert_license_not_called_if_no_license(self, fake_conn):

        with patch("load.insert_license") as fake_insert_license:
            load(fake_conn, {})

            assert fake_insert_license.call_count == 0

    def test_load_insert_license_called_once(self, fake_conn):

        with patch("load.insert_license") as fake_insert_license:
            load(fake_conn, {"license": 44})

            assert fake_insert_license.call_count == 1

    def test_load_insert_images_not_called_if_no_images(self, fake_conn):

        with patch("load.insert_images") as fake_insert_images:
            load(fake_conn, {})

            assert fake_insert_images.call_count == 0

    def test_load_insert_images_called_once(self, fake_conn):

        with patch("load.insert_images") as fake_insert_images:
            load(fake_conn, {"images": "image.png"})

            assert fake_insert_images.call_count == 1

    def test_load_insert_origin_location_not_called_if_no_origin_location(self, fake_conn):

        with patch("load.insert_origin_location") as fake_insert_origin_location:
            load(fake_conn, {})

            assert fake_insert_origin_location.call_count == 0

    def test_load_insert_origin_location_called_once(self, fake_conn):

        with patch("load.insert_origin_location") as fake_insert_origin_location:
            load(fake_conn, {"origin_location": "Birmingham"})

            assert fake_insert_origin_location.call_count == 1

    def test_load_insert_botanist_not_called_if_no_botanist(self, fake_conn):

        with patch("load.insert_botanist") as fake_insert_botanist:
            load(fake_conn, {})

            assert fake_insert_botanist.call_count == 0

    def test_load_insert_botanist_not_called_once(self, fake_conn):

        with patch("load.insert_botanist") as fake_insert_botanist:
            load(fake_conn, {"botanist": "tracy"})

            assert fake_insert_botanist.call_count == 1

    def test_load_insert_plant_not_called_if_no_plant(self, fake_conn):

        with patch("load.insert_plant") as fake_insert_plant:
            load(fake_conn, {})

            assert fake_insert_plant.call_count == 0

    def test_load_insert_plant_not_called_once(self, fake_conn):

        with patch("load.insert_plant") as fake_insert_plant:
            load(fake_conn, {"plant": "daisy"})

            assert fake_insert_plant.call_count == 1

    def test_load_insert_plant_health_not_called_if_no_plant_health(self, fake_conn):

        with patch("load.insert_plant_health") as fake_insert_plant_health:
            load(fake_conn, {})

            assert fake_insert_plant_health.call_count == 0

    def test_load_insert_plant_health_not_called_once(self, fake_conn):

        with patch("load.insert_plant_health") as fake_insert_plant_health:
            load(fake_conn, {"plant_health": "dead"})

            assert fake_insert_plant_health.call_count == 1
