#version 330

//
// This is some code that generates procedural noise from a combination of sources and I did not write
//

float hash(vec3 p3) {
    p3 = fract(p3 * 0.1031);
    p3 += dot(p3, p3.zyx + 31.32);
    return fract((p3.x + p3.y) * p3.z);
}

float noise(vec3 x) {
    vec3 i = floor(x);
    vec3 f = fract(x);
    f = f * f * (3.0 - 2.0 * f);

    return mix(mix(mix(hash(i + vec3(0,0,0)), hash(i + vec3(1,0,0)), f.x),
                   mix(hash(i + vec3(0,1,0)), hash(i + vec3(1,1,0)), f.x), f.y),
               mix(mix(hash(i + vec3(0,0,1)), hash(i + vec3(1,0,1)), f.x),
                   mix(hash(i + vec3(0,1,1)), hash(i + vec3(1,1,1)), f.x), f.y), f.z);
}

float fbm(vec3 p) {
    float v = 0.0, a = 0.5;
    for (int i = 0; i < 6; i++) {
        v += a * noise(p);
        p *= 2.0;
        a *= 0.5;
    }
    return v;
}

//
// Utility function for rotation a vector around the y axis
//

mat3 rotY(float a) {
    float c = cos(a), s = sin(a);
    return mat3( c, 0, -s,
                 0, 1,  0,
                 s, 0,  c);
}


//
// Utility function for offsetting a pixel for dithering
//

float bayer4(vec2 cell) {
    const float m[16] = float[16](0.0, 8.0, 2.0, 10.0,
                                  12.0, 4.0, 14.0, 6.0,
                                  3.0, 11.0, 1.0, 9.0,
                                  15.0, 7.0, 13.0, 5.0);
    int x = int(mod(cell.x, 4.0));
    int y = int(mod(cell.y, 4.0));
    return (m[y * 4 + x] + 0.5) / 16.0;
}