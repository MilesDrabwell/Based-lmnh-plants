import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from lambda_script import calculate_cutoff_time, get_old_data, delete_old_data, write_data_to_parquet, handler


class TestCutoffTime:
    def test_calculate_cutoff_time_datetime(self):
        result = calculate_cutoff_time()
        assert isinstance(result, datetime) == True


class TestGetOldData:
    def test_get_old_data_executes_once(self):
        fake_conn = MagicMock()
        fake_cur = MagicMock()

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        fake_cur.fetchall.return_value = [
            {"plant_id": 23, "temperature": 23.44}]

        result = get_old_data(fake_conn, "12/01/2000")

        fake_cur.execute.assert_called_once_with(
            "SELECT * FROM alpha.plant_health WHERE recording_time <= %s",
            ("12/01/2000",)
        )

    def test_get_old_data_returns_list_of_dicts(self):
        fake_conn = MagicMock()
        fake_cur = MagicMock()

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        fake_cur.fetchall.return_value = [
            {"plant_id": 23, "temperature": 23.44}]

        result = get_old_data(fake_conn, "12/01/2000")

        assert isinstance(result, list)
        assert all(isinstance(plant, dict) for plant in result)


class TestDeleteOldData:
    def test_delete_old_data_executes_once(self):
        fake_conn = MagicMock()
        fake_cur = MagicMock()

        fake_conn.cursor.return_value.__enter__.return_value = fake_cur

        result = delete_old_data(fake_conn, "12/01/2000")

        fake_cur.execute.assert_called_once_with(
            "DELETE FROM alpha.plant_health WHERE recording_time <= %s",
            ("12/01/2000",)
        )
