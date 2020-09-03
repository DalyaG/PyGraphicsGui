#version 330

in vec2 fragment_uv;

uniform sampler2D texture_idx;

out vec4 fragment_color;

void main() {

    fragment_color = texture(texture_idx, fragment_uv);
}