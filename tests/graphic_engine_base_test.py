from unittest import TestCase

from PIL import Image
from mock import patch
from src.graphic_engine.graphic_engine import GraphicEngine


class ProgramVariable:
    def __init__(self, value=None):
        self.value = value

    def write(self, value=None):
        pass


class GraphicEngineBaseTest(TestCase):

    @patch("src.graphic_engine.graphic_engine.GraphicEngine.on_resize")
    @patch("src.graphic_engine.graphic_engine_initializer.GraphicEngineInitializer.load_image_to_texture")
    @patch("src.graphic_engine.graphic_engine_initializer.GraphicEngineInitializer.init_program")
    @patch("src.graphic_engine.graphic_engine_initializer.GraphicEngineInitializer.init_vertex_array")
    def setUp(self, mock_init_vertex_array, mock_init_program, mock_load_image_to_texture, mock_on_resize):
        mock_init_vertex_array.return_value = None
        mock_init_program.return_value = {'texture_idx': ProgramVariable()}
        mock_load_image_to_texture.return_value = None
        mock_on_resize.return_value = None

        self.graphic_engine = GraphicEngine(None, (0, 0), Image.new('RGB', (0, 0), (0, 0, 0)))

    def test_something(self):
        self.assertEqual(1, 1)
