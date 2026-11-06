uniform vec2 iResolution;
uniform float iTime;
uniform float seed;

int pixelCount = 80;
float radius = 0.7;
float cloudRadius = 0.75;
float cloudCoverage = 0.3;
float waterCoverage = 0.5;
float rotationsPerSecond = 0.01;

out vec4 fragColor;

vec3 space = vec3(0.0, 0.0, 0.0);
vec3 ocean = vec3(0.0, 0.3, 0.6);
vec3 land = vec3(0.1, 0.6, 0.2);
vec3 cloud = vec3(1.0, 1.0, 1.0);

void main() {

    fragColor = vec4(space, 1.0);

    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    vec2 p  = (2.0 * gl_FragCoord.xy - iResolution) / iResolution.y;

    //make p pixelated
    
    p = floor(p * float(pixelCount)) / float(pixelCount);

    float z = sqrt(radius * radius - p.x * p.x - p.y * p.y);
    vec3 pos = vec3(p, z) / radius;

    pos = rotY(iTime * rotationsPerSecond * 2 * 3.14159265358979323846264338327950) * pos;

    bool isInsidePlanet = radius * radius > p.x * p.x + p.y * p.y;
    if (isInsidePlanet) {
        float h = fbm(pos * 2.5 + seed);
        if(h < waterCoverage)
            fragColor = vec4(ocean, 1.0);
        else
            fragColor = vec4(land, 1.0);

    }

    z = sqrt(cloudRadius * cloudRadius - p.x * p.x - p.y * p.y);
    vec3 cloudPos = vec3(p, z) / cloudRadius;
    cloudPos = rotY(iTime * rotationsPerSecond * 2 * 3.14159265358979323846264338327950) * cloudPos;

    bool isInsideCloud = cloudRadius * cloudRadius > p.x * p.x + p.y * p.y;
    if (isInsideCloud) {
        
        float h = fbm(cloudPos * 2.5 + seed);
        if(h < cloudCoverage)
            fragColor = vec4(cloud, 1.0);

        if(!isInsidePlanet) {
            vec3 tempPos = vec3(p, -z);
            tempPos = rotY(iTime * rotationsPerSecond * 2 * 3.14159265358979323846264338327950) * tempPos;
            h = fbm(tempPos * 2.5 + seed);
            if(h < cloudCoverage)
                fragColor = vec4(cloud, 1.0);
        }
    }
}