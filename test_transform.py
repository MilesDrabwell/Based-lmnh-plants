import pytest
from transform import check_for_error


@pytest.mark.parametrize('plant_dict', [{'error': True}, 'fake_dict', {'temp': 21, 'time': 20}, {'plant_id': -1}, {'plant_id': '12'}])
def test_check_errors(plant_dict):
    assert check_for_error(plant_dict) == False


@pytest.mark.parametrize('plant_dict', [{'plant_id': 1}, {'plant_id': 40}, {'plant_id': 1000000}])
def test_check_errors_true(plant_dict):
    assert check_for_error(plant_dict) == True


@pytest.mark.parametrize('plant_dict', [{'error': True}, 'fake_dict', {'temp': 21, 'time': 20}])
def test_get_plant_data(plant_dict):
    assert check_for_error(plant_dict) == False
