import os
import random
from utils import hex_to_rgb
from loader import render

MODE = "random"

if MODE == "random":
    files = os.listdir("palettes")
    palette_file = random.choice(files)
    with open(os.path.join("palettes", palette_file)) as f:
        palette = f.read()
        palette = palette.splitlines()
        print(palette)
    settings = {
        "pixelCount": 100,
        "radius": 0.7,
        "cloudRadius": 0.8,
        "cloudCoverage": 0.5,
        "cloudRotationsPerSecond": 0.015,
        "cloudDriftPerSecond": 0.05,
        "waterCoverage": 0.5,
        "sandCoverage": 0.02,
        "rotationsPerSecond": 0.01,
        "ambientLight": 0.05,
        "lightRotationPerSecond": 0.01,
        "bands": True,
        "ditherAmount": 0.5,
        "lightBooster": 0.2,
        "space": (0, 0, 0),
        "ocean": hex_to_rgb(random.choice(palette)),
        "sand": hex_to_rgb(random.choice(palette)),
        "land": hex_to_rgb(random.choice(palette)),
        "cloud": (*hex_to_rgb(random.choice(palette)), 0.8),
    }
    render(settings)

elif MODE == "default":
    render()