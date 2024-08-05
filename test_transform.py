import pytest
from unittest.mock import patch
from transform import check_for_error, get_botanist_data


@pytest.fixture
def botanist_dict_in_db():
    return {'botanist': 'McTesty'}


@pytest.fixture
def botanist_dict_not_in_db():
    return {'botanist': 'Barbara'}


@pytest.fixture
def botanist_database():
    return {'McTesty': 1}


class TestCheckErrors:
    @pytest.mark.parametrize('plant_dict', [{'error': True}, 'fake_dict', {'temp': 21, 'time': 20}, {'plant_id': -1}, {'plant_id': '12'}])
    def test_check_errors(self, plant_dict):
        assert check_for_error(plant_dict) == False

    @pytest.mark.parametrize('plant_dict', [{'plant_id': 1}, {'plant_id': 40}, {'plant_id': 1000000}])
    def test_check_errors_true(self, plant_dict):
        assert check_for_error(plant_dict) == True


class TestBotanist:
    @patch('transform.get_botanist_mapping')
    def test_get_botanist_data_botanist_exists(self, mock_map_botanist, botanist_dict_in_db, botanist_database):
        mock_map_botanist.return_value = botanist_database

        return_value = get_botanist_data(botanist_dict_in_db, 0)
        assert isinstance(return_value) == tuple
        assert return_value[0] == 1

    @patch('transform.get_botanist_mapping')
    def test_get_botanist_data_botanist_new(self, mock_map_botanist, botanist_dict_not_in_db, botanist_database):
        mock_map_botanist.return_value = botanist_database

        return_value = get_botanist_data(botanist_dict_not_in_db, 0)
        assert isinstance(return_value) == tuple
        assert return_value[0] == 2

        return_value_2 = get_botanist_data(botanist_dict_not_in_db, 0)
        assert return_value_2[0] == 2
