uniform vec2 iResolution;
uniform float iTime;
uniform float seed;

//general settings
int pixelCount = 100;

//planet settings
float radius = 0.7;

//cloud settings
float cloudRadius = 0.75;
float cloudCoverage = 0.5;
float cloudRotationsPerSecond = 0.015;
float cloudDriftPerSecond = 0.05;

//surface settings
float waterCoverage = 0.5;
float sandCoverage = 0.02;
float rotationsPerSecond = 0.01;

//light settings
float ambientLight = 0.05;
float lightRotationPerSecond = 0.01;
bool bands = true;
float ditherAmount = 0.5;
float lightBooster = 0.2;

out vec4 fragColor;

vec3 space = vec3(0.0, 0.0, 0.0);
vec3 ocean = vec3(0.0, 0.3, 0.6);
vec3 sand = vec3(0.8, 0.7, 0.5);
vec3 land = vec3(0.1, 0.6, 0.2);
vec4 cloud = vec4(1.0, 1.0, 1.0, 0.8);

void main() {

    fragColor = vec4(space, 1.0);

    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    vec2 p  = (2.0 * gl_FragCoord.xy - iResolution) / iResolution.y;

    //make p pixelated
    
    p = floor(p * float(pixelCount)) / float(pixelCount);

    float z = sqrt(radius * radius - p.x * p.x - p.y * p.y);
    vec3 pos = vec3(p, z) / radius;

    pos = rotY(-iTime * rotationsPerSecond * 2 * 3.14159265358979323846264338327950) * pos;

    bool isInsidePlanet = radius * radius > p.x * p.x + p.y * p.y;
    if (isInsidePlanet) {
        float h = fbm(pos * 2.5 + seed);
        if(h < waterCoverage)
            fragColor = vec4(ocean, 1.0);
        else if(h < waterCoverage + sandCoverage)
            fragColor = vec4(sand, 1.0);
        else
            fragColor = vec4(land, 1.0);

    }

    z = sqrt(cloudRadius * cloudRadius - p.x * p.x - p.y * p.y);
    vec3 cloudPos = vec3(p, z) / cloudRadius;
    cloudPos = rotY(-iTime * cloudRotationsPerSecond * 2 * 3.14159265358979323846264338327950) * cloudPos;
    cloudPos += vec3(0.0, 0.0, iTime * cloudDriftPerSecond);

    bool isInsideCloud = cloudRadius * cloudRadius > p.x * p.x + p.y * p.y;
    if (isInsideCloud) {
        
        float h = fbm(cloudPos * 2.5 + seed + 1);
        if(h < cloudCoverage) {
            vec3 rgb = mix(fragColor.rgb, cloud.rgb, cloud.a);
            fragColor = vec4(rgb, 1.0);
        }
        if(!isInsidePlanet) {
            vec3 tempPos = vec3(p, -z) / cloudRadius;
            tempPos = rotY(-iTime * cloudRotationsPerSecond * 2 * 3.14159265358979323846264338327950) * tempPos;
            tempPos += vec3(0.0, 0.0, iTime * cloudDriftPerSecond);
            h = fbm(tempPos * 2.5 + seed + 1);
            if(h < cloudCoverage) {
                vec3 rgb = mix(fragColor.rgb, cloud.rgb, cloud.a);
                fragColor = vec4(rgb, 1.0);
            }
        }
    }

    vec3 lightDirection = normalize(vec3(1.0, 0.3, 0.3));
    lightDirection = mat3(rotY(-iTime * lightRotationPerSecond * 2 * 3.14159265358979323846264338327950)) * lightDirection;

    pos = vec3(p, z) / radius;
    vec3 normal = normalize(pos);
    
    vec2 cell = floor(p * float(pixelCount) + 0.5); 
    float diffuse = max(min(dot(normal, lightDirection) + lightBooster, 1.0), ambientLight);
    if (bands) {
        diffuse = max(floor(min((dot(normal, lightDirection) + lightBooster), 1.0) * 3.0 + bayer4(cell) * ditherAmount) / 3.0, ambientLight);
    }
    fragColor.rgb *= diffuse;
}