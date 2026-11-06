#version 330

uniform vec2 iResolution;
uniform float iTime;
uniform float seed;

out vec4 fragColor;

vec3 colorOn = vec3(1.0, 1.0, 1.0);
vec3 colorOff = vec3(0.0, 0.0, 0.0);

void main() {

    gl_FragColor = vec4(colorOff, 1.0);

    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    vec2 p  = (2.0 * gl_FragCoord.xy - iResolution) / iResolution.y;

    float maxDist = 0.7;
    if (maxDist * maxDist > p.x * p.x + p.y * p.y) {
        gl_FragColor = vec4(colorOn, 1.0);
    }
}