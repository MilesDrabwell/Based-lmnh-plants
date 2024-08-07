"Testing the functionality of fetch_data.py"
from unittest.mock import patch, AsyncMock
import pytest
from pipeline.extract import get_api_plant_data, new_plant_ids

NUMBER_OF_PLANTS = 50


@pytest.fixture
def plant_example():
    """Creating a fixture with an example of a response expected from the request"""
    return {
        "plant_id": 1,
        "recording_taken": "2024-08-05 11:18:29",
        "soil_moisture": 24.1758099320866,
        "temperature": 12.0237350427114,
    }


class MockHTTPResponse:
    """Want our mock response to be convertible to json as that is a part of the function does"""

    def __init__(self, json_data):
        self._json_data = json_data

    async def json(self, content_type=None):
        "Converting to json?"
        return self._json_data


class TestPlantData:
    @pytest.mark.asyncio
    async def test_async_function_returns_response(self, plant_example):
        """Mock the return value for asyncio.gather and test what happens when it's called"""
        plant_ids = list(range(NUMBER_OF_PLANTS))
        mock_responses = [MockHTTPResponse(plant_example)] * NUMBER_OF_PLANTS

        with patch(
            "asyncio.gather", AsyncMock(return_value=mock_responses)
        ) as patch_gather:
            responses = await get_api_plant_data(plant_ids)
            assert len(responses) == NUMBER_OF_PLANTS
            assert patch_gather.called
            assert patch_gather.call_count == 1

    @pytest.mark.asyncio
    async def test_error_when_wrong(self):
        """Raises error as does not allow plants that do not exist"""
        mock_responses = [MockHTTPResponse(plant_example)] * 20
        with patch(
            "asyncio.gather", AsyncMock(return_value=mock_responses)
        ) as patch_gather:
            with pytest.raises(TypeError):
                assert await get_api_plant_data("a")
                assert await get_api_plant_data({"plant_id"})
                assert await get_api_plant_data(2)


class TestNewPlantIds:
    def test_plant_ids_returned(self):
        plant_data = [
            {"plant_id": 1},
            {"plant_id": 2, "error": "sensor not found"},
            {"plant_id": 3},
            {"plant_id": 4},
            {"plant_id": 5},
        ]
        return_data = [1, 2, 3, 4, 5, 6]
        assert new_plant_ids(plant_data) == return_data

    def test_plant_ids_remove_plant(self):
        plant_data = [
            {"plant_id": 1},
            {"plant_id": 2, "error": "plant not found"},
            {"plant_id": 3},
            {"plant_id": 4},
            {"plant_id": 5},
        ]

        return_data = [1, 3, 4, 5, 6]

        assert new_plant_ids(plant_data) == return_data
