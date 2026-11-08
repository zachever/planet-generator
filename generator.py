
import os
import random
from utils import hex_to_rgb

def generate_random_planet(seed=None):
    files = os.listdir("palettes")
    if seed is not None:
        random.seed(seed)
    palette_file = random.choice(files)
    with open(os.path.join("palettes", palette_file)) as f:
        palette = f.read()
        palette = palette.splitlines()
        print(palette)

    size = 1 + 5 * random.random() ** 3

    radius = random.random() * 0.2 + 0.65
    cloudRadius = random.random() * 0.12 + radius

    rotations_per_second = random.random() * 0.02 + 0.01
    settings = {
        "pixelCount": 100,
        "seed": random.random() * 100.0,
        "size": size,
        "radius": radius,
        "cloudRadius": cloudRadius,
        "cloudCoverage": 0.0 if random.random() < 0.5 else random.random() * 0.2 + 0.3,
        "cloudRotationsPerSecond": rotations_per_second + random.random() * 0.02,
        "cloudDriftPerSecond": random.random() * 0.1,
        "waterCoverage": random.random() * 0.2 + 0.3,
        "sandCoverage": random.random() * 0.2,
        "rotationsPerSecond": rotations_per_second,
        "ambientLight": 0.05,
        "lightRotationPerSecond": random.random() * 0.02 + 0.005,
        "bands": True,
        "ditherAmount": 0.5,
        "lightBooster": 0.2,
        "space": (0, 0, 0),
        "ocean": hex_to_rgb(random.choice(palette)),
        "sand": hex_to_rgb(random.choice(palette)),
        "land": hex_to_rgb(random.choice(palette)),
        "cloud": (*hex_to_rgb(random.choice(palette)), 0.8),
    }
    return settings

