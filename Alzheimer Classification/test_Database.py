from unittest import TestCase

from Database import Database
import PIL.Image as Image
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.image import rgb_to_grayscale
import io


class TestDatabase(TestCase):


    def test_get_assert_files_from_postgresql(self):

        db = Database()
        db.connection()
        print("Connection established")

        db.get_image_path()
        path_of_test_image = db.path + "\\test_image.jfif"

        # image before database:
        temp_img = Image.open(path_of_test_image).resize((180, 180)).convert('L')


        # resized_img = io.BytesIO()
        # temp_img.save(resized_img, format='JPEG')
        # img = resized_img.getvalue()
        print(temp_img)
        #
        # print(np.shape(rgb_to_grayscale(temp_img)))
        # print(np.mean(rgb_to_grayscale(temp_img)))

        print(np.shape(temp_img))
        print(np.mean(temp_img))


        # print(temp_img.getpixel([0, 0]))

        # plt.figure()
        # plt.imshow(temp_img)
        # print(np.mean(temp_img))
        # plt.grid(False)
        # plt.show()

        # image after database:
        assert_images, assert_labels = db.get_assert_files_from_postgresql()

        print(np.mean(assert_images[0]))
        print(np.shape(assert_images[0]))

        # assert -> Pixel oben rechts (Orginial) = Pixel oben rechts (nach Datenbank)
        decimalPlace = 1
        self.assertAlmostEqual(np.mean(temp_img), np.mean(assert_images[0]), decimalPlace)
