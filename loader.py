import os
import random
import time
 
import moderngl
import numpy as np
import pygame
 
W, H = 800, 800
FRAG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planet.frag")
UTILS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils.glsl")

# simply render a quad to allow fragment shader to run for each pixel
VERT = """
#version 330
in vec2 in_pos;
void main() { gl_Position = vec4(in_pos, 0.0, 1.0); }
"""

SETTINGS = {
    # general
    "pixelCount": 100,
 
    # planet
    "radius": 0.7,
 
    # clouds
    "cloudRadius": 0.75,
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
 
 

def render(settings=None):
    if settings is None:
        settings = SETTINGS
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