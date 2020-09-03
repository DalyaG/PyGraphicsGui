from tests.graphic_engine_base_test import GraphicEngineBaseTest


class TestMathematicalCalculations(GraphicEngineBaseTest):

    def test_window_pixel_coordinates_to_image_pixel_coordinates(self):
        self.graphic_engine._image_size_pixels = [48, 48]
        self.graphic_engine._window_width_pixels, self.graphic_engine._window_height_pixels = 12, 12

        self.assertEqual((0, 0), self.graphic_engine.window_pixel_coordinates_to_image_pixel_coordinates(0, 0))
        self.assertEqual((48, 24), self.graphic_engine.window_pixel_coordinates_to_image_pixel_coordinates(12, 6))

    def test_window_pixels_coordinates_to_xy_coordinates(self):
        self.graphic_engine._image_size_pixels = [48, 48]
        self.graphic_engine._window_width_pixels, self.graphic_engine._window_height_pixels = 12, 12

        self.assertEqual((-1.0, 1.0), self.graphic_engine.window_pixels_coordinates_to_xy_coordinates(0, 0))
        self.assertEqual((1.0, 0.0), self.graphic_engine.window_pixels_coordinates_to_xy_coordinates(12, 6))

    def test_xy_coordinates_to_window_pixel_coordinates(self):
        self.graphic_engine._image_size_pixels = [48, 48]
        self.graphic_engine._window_width_pixels, self.graphic_engine._window_height_pixels = 12, 12

        self.assertEqual((0, 0), self.graphic_engine.xy_coordinates_to_window_pixel_coordinates(-1.0, 1.0))
        self.assertEqual((12, 6), self.graphic_engine.xy_coordinates_to_window_pixel_coordinates(1.0, 0.0))
