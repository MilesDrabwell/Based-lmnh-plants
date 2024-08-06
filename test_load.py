from unittest.mock import patch
from load import insert_license, insert_images, insert_origin_location, insert_botanist, insert_plant_health, insert_plant, load

# Test how many times things get called. Test if one does not exist, it does not get called.
