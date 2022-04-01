import concurrent.futures
import threading

import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glBegin, GL_LINES, glVertex3fv, glEnd, glTranslatef, glClear, GL_COLOR_BUFFER_BIT, \
    GL_DEPTH_BUFFER_BIT, glRotatef
from OpenGL.GLU import gluPerspective

from data_struct.General import Faces
import math
import numpy as np


RATIO = 10

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


def robot_to_world(robot_in_world_angle, robot_in_world_x, robot_in_world_y, object_in_robot_x, object_in_robot_y):  # Angle en degré
    alpha = math.radians(robot_in_world_angle)  # Conversion en rad
    pos_robot_in_world = np.array([robot_in_world_x, robot_in_world_y])  # Position Robot dans le repère Monde
    pos_object_in_robot = np.array([object_in_robot_x, object_in_robot_y])  # Position objet dans le repère Robot
    R = np.array([[math.cos(alpha), math.sin(-alpha)], [math.sin(alpha), math.cos(alpha)]])
    return R @ pos_object_in_robot + pos_robot_in_world


def draw_kapla(pos, angle, face: Faces):
    kapla_edges = []
    kapla_vertices = []
    x, z, y = pos

    # Get how is the Kapla
    shift_x, shift_y, shift_z = 0, 0, 0
    if face == Faces.big_face:
        shift_x, shift_y, shift_z = 70, 20, 25
    elif face == Faces.small_face:
        shift_x, shift_y, shift_z = 25, 70, 20
    elif face == Faces.medium_face:
        shift_x, shift_y, shift_z = 70, 25, 20

    # Add the points

    x = x / RATIO
    y = y / RATIO
    z = z / RATIO
    shift_x = shift_x / RATIO
    shift_y = shift_y / RATIO
    shift_z = shift_z / RATIO


    kapla_vertices.append((x, y, z))
    kapla_vertices.append((x, y, z + shift_z))
    kapla_vertices.append((x, y + shift_y, z + shift_z))
    kapla_vertices.append((x, y + shift_y, z))
    kapla_vertices.append((x + shift_x, y + shift_y, z))
    kapla_vertices.append((x + shift_x, y + shift_y, z + shift_z))
    kapla_vertices.append((x + shift_x, y, z + shift_z))
    kapla_vertices.append((x + shift_x, y, z))

    kapla_edges.append((0, 1))
    kapla_edges.append((1, 2))
    kapla_edges.append((2, 3))
    kapla_edges.append((3, 0))

    kapla_edges.append((7, 6))
    kapla_edges.append((6, 5))
    kapla_edges.append((5, 4))
    kapla_edges.append((4, 7))

    kapla_edges.append((0, 7))
    kapla_edges.append((1, 6))
    kapla_edges.append((2, 5))
    kapla_edges.append((3, 4))

    for i in range(len(kapla_vertices)):
        tx, ty, tz = kapla_vertices[i]
        tx, tz = robot_to_world(angle, x, z, tx, tz)
        kapla_vertices[i] = (tx, ty, tz)

    return kapla_edges, kapla_vertices


def display_structure(edges, vertices):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def add_edges(edges, vertices, added_edges, added_vertices):

    len_vertices = len(vertices)
    vertices += added_vertices
    for edge in added_edges:
        edges.append((edge[0] + len_vertices, edge[1] + len_vertices))


def pygame_drawer():

    pygame.init()
    display = (1080, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
    glTranslatef(0.0, -10, -30)

    # HACKING HAHAHA
    from logic.KaplaOrganizer import get_sequence
    sequence = list(get_sequence())

    tmp = 30
    count = 0
    index = 1
    max_size = len(sequence)

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
        kapla_to_draw = sequence[:index]
        edges, vertices = [], []

        if count > tmp:
            index += 1
            count = 0
        if index > max_size:
            index = 0
        count += 1

        for kapla in kapla_to_draw:
            temp_edges, temp_vertices = draw_kapla(*kapla)
            add_edges(edges, vertices, temp_edges, temp_vertices)

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


if __name__ == "__main__":
    pygame_drawer()