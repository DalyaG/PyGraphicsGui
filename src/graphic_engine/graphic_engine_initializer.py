import os
from pathlib import Path

import glm
import moderngl
import numpy as np
from PIL import Image
from src.logging_utils import get_logger


class GraphicEngineInitializer:
    SHADERS_FOLDER_NAME = "shaders"
    VERTEX_SHADER_FILENAME = "vertex_shader.glsl"
    FRAGMENT_SHADER_FILENAME = "fragment_shader.glsl"

    def __init__(self):
        self._logger = get_logger()
        self.shaders_folder = os.path.join(Path(__file__).parent, self.SHADERS_FOLDER_NAME)

    def load_image_to_texture(self, context: moderngl.Context, image: Image) -> moderngl.Texture:
        texture = context.texture(image.size, 3, image.tobytes())
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.use(0)
        self._logger.debug(f"Loaded image of size {texture.size} to texture")
        return texture

    def init_program(self, context: moderngl.Context):
        with open(os.path.join(self.shaders_folder, self.VERTEX_SHADER_FILENAME), 'r') as f:
            vertex_shader = f.read()
        with open(os.path.join(self.shaders_folder, self.FRAGMENT_SHADER_FILENAME), 'r') as f:
            fragment_shader = f.read()
        program = context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        program['model'].write(bytes(glm.mat4()))
        return program
    
    def init_vertex_array(self, context: moderngl.Context, program: moderngl.Program) -> moderngl.VertexArray:
        vertices_xy = self.get_vertices_for_quad_2d(size=(2.0, 2.0), bottom_left_corner=(-1.0, -1.0))
        vertex_buffer_xy = context.buffer(vertices_xy.tobytes())

        vertices_uv = self.get_vertices_for_quad_2d(size=(1.0, 1.0), bottom_left_corner=(0.0, 0.0))
        vertex_buffer_uv = context.buffer(vertices_uv.tobytes())

        vertex_array = context.vertex_array(program, [(vertex_buffer_xy, "2f", "vertex_xy"),
                                                      (vertex_buffer_uv, "2f", "vertex_uv")])
        return vertex_array

    def get_vertices_for_quad_2d(self, size=(2.0, 2.0), bottom_left_corner=(-1.0, -1.0)) -> np.array:
        # A quad is rectangle composed of 2 triangles: https://en.wikipedia.org/wiki/Polygon_mesh
        w, h = size
        x_bl, y_bl = bottom_left_corner
        vertices = np.array([x_bl,     y_bl + h,
                             x_bl,     y_bl,
                             x_bl + w, y_bl,

                             x_bl,     y_bl + h,
                             x_bl + w, y_bl,
                             x_bl + w, y_bl + h], dtype=np.float32)
        return vertices
