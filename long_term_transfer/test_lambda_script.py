import pytest
from lambda_script import calculate_cutoff_time
from datetime import datetime


class TestCutoffTime:
    def test_calculate_cutoff_time_datetime(self):
        result = calculate_cutoff_time()
        assert isinstance(result, datetime) == True
