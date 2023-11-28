import unittest

from skimage.data._fetchers import immunohistochemistry

from fast_skimage import Image, astronaut_noisy, etretat, walking, camera
from fast_skimage import nyc
from fast_skimage import zebra
from fast_skimage.Image import RED, WHITE, BLUE, GREEN

class ImageTestCase(unittest.TestCase):

    def test_add_watermark(self):
        path_to_nyc, path_to_watermark, path_to_zebra = 'Pictures/nyc.jpg', 'Pictures/watermark.png', 'Pictures/zebra.jpg'

        background_image = Image(path_to_nyc, chatty_mode=True)
        watermark = Image(path_to_watermark, chatty_mode=True)

        background_image.add_watermark(watermark, 0.5, 0.5, wm_color=RED, alpha=0.55, spread=0.5)
        background_image.add_watermark(watermark, 0.2, 0.7, wm_color=WHITE, alpha=0.5, spread=1)
        background_image.add_watermark(watermark, 0.6, 0.1, wm_color=BLUE, alpha=1, spread=2)
        background_image.add_watermark(watermark, 0.3, 0.3, wm_color=GREEN, alpha=1, spread=3)
        background_image.show(title="Marked NYC Picture")

    def test_auto_enhance(self):
        object_image1 = zebra()
        object_image2 = astronaut_noisy()
        object_image3 = nyc()
        object_image4 = etretat()
        object_image5 = walking()
        object_image6 = camera()
        array_image7 = immunohistochemistry()

        imlist = [Image(object_image1.get(), chatty_mode=True), Image(object_image2.get(), chatty_mode=True),
                  Image(object_image3.get(), chatty_mode=True), Image(object_image4.get(), chatty_mode=True),
                  Image(object_image5.get(), chatty_mode=True), Image(object_image6.get(), chatty_mode=True),
                  Image(array_image7, chatty_mode=True)]

        for im in imlist:
            im.show(subplots=(1, 2, 1), size=12, title="Original Image")
            im.auto_enhance()
            im.show(subplots=(1, 2, 2), title="Auto-enhanced Image")

    def test_segmentation(self):
        im = Image('Pictures/mri_brain.jpg', True)
        im.color_to_gray()
        areas = im.gaussian_mixture_segmentation(zones=5, iterations=1000, return_areas=True)
        im.show(colorbar=True, cmap='viridis')

        cm_by_pixel = 0.115
        cm2_by_pixel2 = cm_by_pixel ** 2
        for area in areas:
            if area == min(areas):  # area of interesting zone (after looking at the output)
                print(f"Area of the tumor is estimated to {round(cm2_by_pixel2 * area, 2)} cm².")


if __name__ == '__main__':
    unittest.main()