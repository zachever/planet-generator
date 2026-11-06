import os
import random
import time
 
import moderngl
import numpy as np
import pygame
 
W, H = 800, 800
FRAG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planet.frag")

# simply render a quad to allow fragment shader to run for each pixel
VERT = """
#version 330
in vec2 in_pos;
void main() { gl_Position = vec4(in_pos, 0.0, 1.0); }
"""
 
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
pygame.display.set_mode((W, H), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("planet shader  |  R = new seed")
 
ctx = moderngl.create_context()
 
quad = np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype="f4")
vbo = ctx.buffer(quad.tobytes())
 
 
def load_shader():
    with open(FRAG_PATH) as f:
        src = f.read()
    prog = ctx.program(vertex_shader=VERT, fragment_shader=src)
    vao = ctx.vertex_array(prog, [(vbo, "2f", "in_pos")])
    return prog, vao
 
 
def set_uniform(prog, name, value):
    if name in prog:
        prog[name].value = value
 
 

def render():
    prog, vao = load_shader()
    mtime = os.path.getmtime(FRAG_PATH)
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
    
        ctx.clear()
        vao.render(moderngl.TRIANGLE_STRIP)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()