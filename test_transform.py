import pytest
from transform import check_for_error, get_botanist_data, get_origin_data, get_license_data, get_images_data, get_plant_data, get_health_data


@pytest.fixture
def test_database():
    return {'McTesty': 1, 'FR': 1, 'Universal': 451, 'Universal.com': 451, 'plant_id': 3}


class TestCheckErrors:
    @pytest.mark.parametrize('plant_dict', [{'error': True}, {'temp': 21, 'time': 20}, {'plant_id': -1}, {'plant_id': '12'}])
    def test_check_errors_false(self, plant_dict):
        assert check_for_error(plant_dict) == False

    def test_check_errors_invalid_input(self):
        plant_dict = 'test_str'
        with pytest.raises(AttributeError):
            check_for_error(plant_dict) == False

    @pytest.mark.parametrize('plant_dict', [{'plant_id': 1}, {'plant_id': 40}, {'plant_id': 1000000}])
    def test_check_errors_true(self, plant_dict):
        plant_dict['recording_taken'] = '5 minutes ago'
        assert check_for_error(plant_dict) == True


class TestBotanist:
    def test_get_botanist_data_botanist_not_exists(self, test_database):
        assert get_botanist_data(
            {'name': 'McTesty'}, test_database, {}) == None

    def test_get_botanist_data_botanist_exists(self, test_database):
        assert get_botanist_data(
            {"botanist": {"name": "McTesty"}}, test_database, {}) == None

    def test_get_botanist_data_botanist_new_empty_db(self):
        return_value = get_botanist_data(
            {"botanist": {"name": "Barbara"}}, {}, {'Barbara': 2})
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 2

    def test_get_botanist_data_botanist_new_botanist(self):
        return_value = get_botanist_data(
            {"botanist": {"name": "Thirdy"}}, {'Barbara': 2}, {})
        print(return_value)
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 3


class TestOrigin:
    def test_get_origin_data_origin_location_not_exists(self, test_database):
        assert get_origin_data(
            {'origin': [0, 0, 0, 1]}, test_database, {}) == None

    def test_get_origin_data_origin_location_exists(self, test_database):
        assert get_origin_data(
            {"origin_location": [0, 0, 'france', 'FR']}, test_database, {}) == None

    def test_get_origin_data_origin_new_empty_db(self):
        return_value = get_origin_data(
            {"origin_location": [0, 0, 'great britain', 'GB', 'test/location']}, {}, {'GB': 2})
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 2

    def test_get_origin_data_origin_new_origin(self):
        return_value = get_origin_data(
            {"origin_location": [1, 2, 'Brazil', 'BR', 'test/location']}, {'GB': 2}, {})
        print(return_value)
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 3


class TestLicence:
    def test_get_licence_data_license_not_exists(self, test_database):
        assert get_license_data(
            {'not an image': {'license_name': 'Universal'}}, test_database) == None

    def test_get_license_data_license_exists(self, test_database):
        assert get_license_data(
            {"images": {'license_name': 'Universal'}}, test_database) == None

    def test_get_license_data_license_new_license(self):
        return_value = get_license_data(
            {"images": {'license_name': 'illumination', 'license': 453}}, {'disney': 452})
        print(return_value)
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 453


class TestImages:
    def test_get_images_data_image_not_exists(self, test_database):
        assert get_images_data(
            {'not an image': {'regular_url': 'Universal.com'}}, test_database, {}, {"images": {'license_name': 'Universal'}}) == None

    def test_get_image_data_image_exists(self, test_database):
        assert get_images_data(
            {"images": {'regular_url': 'Universal.com', 'license_name': 'Universal'}}, test_database, {}, {"images": {'license_name': 'Universal'}}) == None

    def test_get_image_data_image_new_empty_db(self):
        return_value = get_images_data(
            {"images": {'regular_url': 'Disney.com', 'license_name': 'Disney'}}, {}, {'Disney.com': 452}, {"images": {'license_name': 'Disney'}})
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 452

    def test_get_image_data_image_new_image(self):
        return_value = get_images_data(
            {"images": {'regular_url': 'illumination.com', 'license_name': 'Universal'}}, {'Disney.com': 452}, {}, {})
        print(return_value)
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 453


class TestPlants:
    def test_get_plant_data_plant_not_exists(self, test_database):
        assert get_plant_data(
            {'not a name': 'test plant'}, test_database, {}, {}, {}, {}, {}, {}) == None

    def test_get_plant_data_plant_exists(self, test_database):
        assert get_plant_data(
            {'name': 'test plant', 'plant_id': 3}, test_database, {}, {}, {}, {}, {}, {}) == None

    def test_get_plant_data_plant_new(self):
        return_value = get_plant_data(
            {'name': 'test plant', 'plant_id': 3, 'scientific_name': ['science_test']}, {'plant_id': 2}, {}, {}, {}, {}, {}, {})
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 3

    def test_get_plant_data_plant_new_other_ids(self):
        return_value = get_plant_data(
            {'name': 'test plant', 'plant_id': 3, 'scientific_name': ['science_test'], 'origin_location': [0, 0, 0, 'GB'], 'botanist': {'name': 'Barbara'}, 'images': {'regular_url': 'Disney.com'}}, {'plant_id': 2}, {'GB': 10}, {}, {'Barbara': 20}, {}, {'Disney.com': 452}, {})
        print()
        assert isinstance(return_value, tuple) == True
        assert return_value[5] == 10
        assert return_value[3] == 20
        assert return_value[4] == 452


class TestPlantHealth:
    def test_get_images_data_image_not_exists(self, test_database):
        assert get_health_data(
            {}) == None

    def test_get_image_data_image_exists(self, test_database):
        assert get_health_data(
            {}, test_database, {}, {"images": {'license_name': 'Universal'}}) == None

    def test_get_image_data_image_new_empty_db(self):
        return_value = get_health_data(
            {})
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 452

    def test_get_image_data_image_new_image(self):
        return_value = get_health_data(
            {})
        print(return_value)
        assert isinstance(return_value, tuple) == True
        assert return_value[0] == 453
