import os
import random
import time
 
import moderngl
import numpy as np
import pygame
import io
from PIL import Image

from generator import generate_random_planet
from save_system import load_planet_from_file, save_planet_to_file
 
W, H = 1000, 1000
FRAG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planet.frag")
UTILS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils.glsl")

# simply render a quad to allow fragment shader to run for each pixel
VERT = """
#version 330
in vec2 in_pos;
void main() { gl_Position = vec4(in_pos, 0.0, 1.0); }
"""

DEFAULT_SETTINGS = {
    # general
    "pixelCount": 100,
 
    # planet
    "size": 1.0, #overall size of the planet, does not alter size on screen, but rather alters internal scale so biomes are smaller given a larger planet
    "radius": 0.7, #mostly just for how large of portion planet takes on screen, 1.0 means planet sides touch edges of screen
 
    # clouds
    "cloudRadius": 0.75, #mostly just for how large of portion clouds takes on screen, 1.0 means clouds touch edges of screen
    "cloudCoverage": 0.5,
    "cloudRotationsPerSecond": 0.015,
    "cloudDriftPerSecond": 0.05,
 
    # surface
    "waterCoverage": 0.5,
    "sandCoverage": 0.02,
    "rotationsPerSecond": 0.01,
 
    # light
    "ambientLight": 0.05,
    "lightRotationPerSecond": 0.01,
    "bands": True,
    "ditherAmount": 0.5,
    "lightBooster": 0.2,
 
    # colours
    "space": (0.0, 0.0, 0.0),
    "ocean": (0.0, 0.3, 0.6),
    "sand": (0.8, 0.7, 0.5),
    "land": (0.1, 0.6, 0.2),
    "cloud": (1.0, 1.0, 1.0, 0.8),
}
 
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
pygame.display.set_mode((W, H), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Planet Generator")
 
ctx = moderngl.create_context()
 
quad = np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype="f4")
vbo = ctx.buffer(quad.tobytes())
 
 
def load_shader():
    with open(UTILS_PATH) as f:
        utils_src = f.read()
    with open(FRAG_PATH) as f:
        frag_src = f.read()

    src = utils_src + "\n" + frag_src
    prog = ctx.program(vertex_shader=VERT, fragment_shader=src)
    vao = ctx.vertex_array(prog, [(vbo, "2f", "in_pos")])
    return prog, vao
 
 
def set_uniform(prog, name, value):
    if name in prog:
        prog[name].value = value
 
def capture_planet(prog, vao, clock, force_lighting=False):
    #set custom photos so that the screenshot
    if force_lighting:
        set_uniform(prog, "iTime", 0)

        ctx.clear()
        vao.render(moderngl.TRIANGLE_STRIP)
        pygame.display.flip()
        #clock.tick(60)

    data = ctx.screen.read(viewport=(0, 0, W, H), components=3)
    image = Image.frombytes("RGB", (W, H), data)
    return image.transpose(Image.FLIP_TOP_BOTTOM)


def render(mode="default"):
    if mode == "default":
        settings = DEFAULT_SETTINGS
    
    elif mode == "random":
        settings = generate_random_planet()
    
    else:
        settings = load_planet_from_file(mode)

    prog, vao = load_shader()
    mtime = os.path.getmtime(FRAG_PATH)
    random.seed(0)
    seed = random.random() * 100.0
    start = time.time()
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_SPACE:
                    settings = generate_random_planet()
                elif e.key == pygame.K_s:
                    screenshot = capture_planet(prog, vao, clock)
                    save_planet_to_file(settings, screenshot)
                elif e.key == pygame.K_r:
                    seed = random.random() * 100.0
    
        m = os.path.getmtime(FRAG_PATH)
        if m != mtime:
            mtime = m
            try:
                prog, vao = load_shader()
                print("shader reloaded")
            except Exception as ex:
                print("shader error:\n", ex)
    
        set_uniform(prog, "iResolution", (float(W), float(H)))
        set_uniform(prog, "iTime", time.time() - start)
        set_uniform(prog, "seed", seed)
        for name, value in settings.items():
            set_uniform(prog, name, value)
    
        ctx.clear()
        vao.render(moderngl.TRIANGLE_STRIP)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()