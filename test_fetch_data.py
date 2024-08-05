from unittest.mock import patch, AsyncMock
from unittest.mock import patch
import pytest
from fetch_data_fast import get_plant_data
import json
# Our test function


@pytest.fixture
def result_1():
    return {
        "botanist": {
            "email": "gertrude.jekyll@lnhm.co.uk",
            "name": "Gertrude Jekyll",
            "phone": "001-481-273-3691x127"
        },
        "last_watered": "Sun, 04 Aug 2024 13:54:32 GMT",
        "name": "Venus flytrap",
        "origin_location": [
            "33.95015",
            "-118.03917",
            "South Whittier",
            "US",
            "America/Los_Angeles"
        ],
        "plant_id": 1,
        "recording_taken": "2024-08-05 11:18:29",
        "soil_moisture": 24.1758099320866,
        "temperature": 12.0237350427114
    }

# Our test function


class MockHTTPResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    async def json(self):
        return self._json_data


@pytest.mark.asyncio
async def test_my_async_function():
    # Mock return value for asyncio.gather

    mock_responses = [MockHTTPResponse(result_1)]
    expected_responses = [result_1]

    with patch('asyncio.gather', AsyncMock(return_value=mock_responses)) as patch_gather:
        responses = await get_plant_data()
        assert responses == expected_responses
        for response in responses:
            assert response['plant_id'] == 1
        assert patch_gather.called  # is actually getting called
        assert patch_gather.call_count == 1  # and only once
