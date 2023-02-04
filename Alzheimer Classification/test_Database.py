from unittest import TestCase

from Database import Database
import PIL.Image as Image
import numpy as np

class TestDatabase(TestCase):

    def test_get_assert_files_from_postgresql(self):
        # create class Database
        db = Database()
        db.connection()
        print("Connection established")

        db.get_image_path()
        path_of_test_image = db.path + "\\test_image.jfif"

        # image before database:
        temp_img = Image.open(path_of_test_image).resize((180, 180)).convert('L')
        mean_image_before = np.mean(temp_img)

        # image after database:
        assert_images, assert_labels = db.get_assert_files_from_postgresql()
        mean_image_after = np.mean(assert_images[0])

        # assert mean values almost equal
        decimalPlace = 1
        self.assertAlmostEqual(mean_image_before, mean_image_after, decimalPlace)
