"Testing the functionality of fetch_data.py"
from unittest.mock import patch, AsyncMock
import pytest
from fetch_data import get_plant_data

NUMBER_OF_PLANTS = 50

@pytest.fixture
def result_1():
    """Creating a fixture with an example of a response expected from the request"""
    return {
        "botanist": {
            "email": "gertrude.jekyll@lnhm.co.uk",
            "name": "Gertrude Jekyll",
            "phone": "001-481-273-3691x127",
        },
        "last_watered": "Sun, 04 Aug 2024 13:54:32 GMT",
        "name": "Venus flytrap",
        "origin_location": [
            "33.95015",
            "-118.03917",
            "South Whittier",
            "US",
            "America/Los_Angeles",
        ],
        "plant_id": 1,
        "recording_taken": "2024-08-05 11:18:29",
        "soil_moisture": 24.1758099320866,
        "temperature": 12.0237350427114,
    }


class MockHTTPResponse:
    """Want our mock response to be convertible to json as that is a part of the function does"""
    def __init__(self, json_data):
        self._json_data = json_data

    async def json(self):
        "Converting to json?"
        return self._json_data


@pytest.mark.asyncio
async def test_async_function_returns_response():
    """Mock the return value for asyncio.gather and test what happens when it's called"""

    mock_responses = [MockHTTPResponse(result_1)]
    expected_responses = [result_1]

    with patch(
        "asyncio.gather", AsyncMock(return_value=mock_responses)
    ) as patch_gather:
        responses = await get_plant_data()
        assert responses == expected_responses
        assert patch_gather.called
        assert patch_gather.call_count == 1


@pytest.mark.asyncio
async def test_error_when_wrong():
    """Raises error as does not allow plants that do not exist"""
    with pytest.raises(TypeError):
        assert await get_plant_data('a')
