import glm
import moderngl
from PIL import Image

from src.graphic_engine.graphic_engine_initializer import GraphicEngineInitializer
from src.logging_utils import get_logger


class GraphicEngine:
    """
    Glossary:

    Window: The main window that shows the image.

    The VIEWPORT of the window, is the portion of the image that is visible through the window.

    _pixels (suffix): Indicates the variable is of type int, 0 <= p_x <= width, 0 <= p_y <= height.
                      The coordinates are [0,0] on the top left of the screen, and [width, height] on the bottom right.
                      Notice you have two different types of pixel coordinates - for the window and for the image.
    _xy (suffix): Indicates the variable is of type float, -1 <= x <= 1, -1 <= y <= 1.
                  The coordinates are [-1, -1] on the bottom left of the screen, and [1, 1] on the top right.
                  This corresponds to the "window" coordinate system, where (0, 0) is the center.
    _uv (suffix): Indicates the variable is of type float, 0 <= u <= 1, 0 <= v <= 1.
                  The coordinates are [0, 0] on the bottom left of the screen, and [1, 1] on the top right.
                  This corresponds to the "image" coordinate system, where (0.5, 0.5) is the center.

    """
    def __init__(self, context: moderngl.Context, window_size_pixels: (int, int), image: Image):
        self._logger = get_logger()

        self._context = context

        initializer: GraphicEngineInitializer = GraphicEngineInitializer()

        self._image_size_pixels: Image = image.size
        self._texture: moderngl.Texture = initializer.load_image_to_texture(self._context, image)

        self._program: moderngl.Program = initializer.init_program(self._context)
        self._program['texture_idx'].value = 0
        self._window_model_mat: glm.mat4 = glm.mat4()

        self._vertex_array: moderngl.VertexArray = initializer.init_vertex_array(self._context, self._program)

        self._window_width_pixels, self._window_height_pixels = window_size_pixels

    def destroy(self):
        self._texture.release()

    def clear(self, color=(0, 0, 0, 0)):
        self._context.clear(*color)

    def render(self):
        self._program['model'].write(bytes(self._window_model_mat))
        self._vertex_array.render()

    def on_resize(self, new_size_pixels: (int, int)):
        self._window_width_pixels, self._window_height_pixels = new_size_pixels
        self._logger.debug(f"Updated windows after resize. New size: {new_size_pixels}.")

    def window_pixel_coordinates_to_image_pixel_coordinates(self, x_window_pixels: int, y_window_pixels: int) -> (int, int):
        x, y = self.window_pixels_coordinates_to_xy_coordinates(x_window_pixels, y_window_pixels)
        u = (0.5 * x) + 0.5
        v = (0.5 * y) + 0.5

        x_image_pixels = int(u * self._image_width_pixels)
        y_image_pixels = int((1 - v) * self._image_height_pixels)
        return x_image_pixels, y_image_pixels

    def window_pixels_coordinates_to_xy_coordinates(self, x_pixels: int, y_pixels: int) -> (float, float):
        # x_pixels,y_pixels are represented in pixels from the top left corner,
        # viewport coordinates are represented in [-1,1]X[-1,1] starting at bottom left corner at (-1,-1)
        u, one_minus_v = x_pixels / self._window_width_pixels, y_pixels / self._window_height_pixels
        # Now we have coordinates in [0,1]X[0,1], but still starting at top left at (0,0)
        # So we want to make the transformation [0,1]X[0,1] => [1,-1]X[-1,1]
        x_window = (u * 2) - 1.0
        y_window = ((1.0 - one_minus_v) * 2) - 1.0
        x, y = (glm.inverse(self._window_model_mat) * glm.vec4(x_window, y_window, 0, 1)).xy
        return x, y

    def xy_coordinates_to_window_pixel_coordinates(self, x: float, y: float) -> (int, int):
        x_window, y_window = (self._window_model_mat * glm.vec4(x, y, 0, 1)).xy
        if not((-1 <= x_window <= 1) and (-1 <= y_window <= 1)):
            return None

        u_window = (0.5 * x_window) + 0.5
        v_window = (0.5 * y_window) + 0.5

        x_pixels = int(u_window * self._window_width_pixels)
        y_pixels = int((1 - v_window) * self._window_height_pixels)

        return x_pixels, y_pixels

    @property
    def _image_width_pixels(self):
        return self._image_size_pixels[0]

    @property
    def _image_height_pixels(self):
        return self._image_size_pixels[1]

    @property
    def _window_size_pixels(self):
        return self._window_width_pixels, self._window_height_pixels
