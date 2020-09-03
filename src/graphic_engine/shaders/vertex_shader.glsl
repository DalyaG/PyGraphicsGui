#version 330

in vec2 vertex_xy;
in vec2 vertex_uv;

uniform mat4 model;

out vec2 fragment_uv;

void main() {
    vec4 p = vec4(vertex_xy, 0.0, 1.0);
    gl_Position = model * p;
    fragment_uv = vertex_uv;
}