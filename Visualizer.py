import concurrent.futures
import threading

import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glBegin, GL_LINES, glVertex3fv, glEnd, glTranslatef, glClear, GL_COLOR_BUFFER_BIT, \
    GL_DEPTH_BUFFER_BIT, glRotatef
from OpenGL.GLU import gluPerspective

from data_struct.General import Faces


# https://realpython.com/intro-to-python-threading/
class Pipeline:
    def __init__(self):
        self.content = []
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()

    def get_content(self):
        self.consumer_lock.acquire()
        content = self.content
        self.consumer_lock.release()
        return content

    def set_content(self, content):
        self.producer_lock.acquire()
        self.content = content
        self.producer_lock.release()


def draw_kapla(pos, angle, face: Faces):
    kapla_edges = []
    kapla_vertices = []
    x, y, z = pos

    # Get how is the Kapla
    shift_x, shift_y, shift_z = 0, 0, 0
    if face == face.big_face:
        shift_x, shift_y, shift_z = 20, 70, 24
    elif face == face.medium_face:
        shift_x, shift_y, shift_z = 24, 70, 20
    elif face == face.small_face:
        shift_x, shift_y, shift_z = 70, 24, 20

    # Add the points

    kapla_edges.append((x, y, z))
    kapla_edges.append((x, y, z + shift_z))
    kapla_edges.append((x, y + shift_y, z + shift_z))
    kapla_edges.append((x, y + shift_y, z))
    kapla_edges.append((x + shift_x, y + shift_y, z))
    kapla_edges.append((x + shift_x, y + shift_y, z + shift_z))
    kapla_edges.append((x + shift_x, y, z + shift_z))
    kapla_edges.append((x + shift_x, y, z))

    kapla_vertices.append((0, 1))
    kapla_vertices.append((1, 2))
    kapla_vertices.append((2, 3))
    kapla_vertices.append((3, 0))

    kapla_vertices.append((7, 6))
    kapla_vertices.append((6, 5))
    kapla_vertices.append((5, 4))
    kapla_vertices.append((4, 7))

    kapla_vertices.append((0, 7))
    kapla_vertices.append((1, 6))
    kapla_vertices.append((2, 5))
    kapla_vertices.append((3, 4))

    return kapla_edges, kapla_vertices


def display_structure(edges, vertices):
    glBegin(GL_LINES)
    for i in range(len(edges)):
        for edge in edges[i]:
            for vertex in edge:
                glVertex3fv(vertices[i][vertex])
    glEnd()


def pygame_drawer(pipeline: Pipeline):

    pipeline.get_content()
    pygame.init()
    display = (1080, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
    glTranslatef(0.0, -3, -15)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(1, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-1, 0, 0)

                if event.key == pygame.K_UP:
                    glTranslatef(0, 0, 1)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 0, -1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, -0.2, 0)
                if event.button == 5:
                    glTranslatef(0, 0.2, 0)
        kapla_to_draw = pipeline.get_content()
        edges, vertices = [], []

        print(f"")

        for kapla in kapla_to_draw:
            temp_edges, temp_vertices = draw_kapla(*kapla)
            edges.append(temp_edges)
            vertices.append(temp_vertices)

        # Update edges and vertices
        print(f"edges : {len(edges)}, vertices {len(vertices)}, len kapla : {len(kapla_to_draw)}")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        display_structure(edges, vertices)
        glRotatef(1, 0, 1, 0)
        pygame.display.flip()
        pygame.time.wait(15)



def visualize(producer):
    pipeline = Pipeline()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(pygame_drawer, pipeline)

