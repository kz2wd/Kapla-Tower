import json
import copy


def get_sequence():
    with open('resources/construction.json') as json_data:
        data = json.load(json_data)
        kapla_list = copy.deepcopy(data)

    list_size = len(kapla_list)
    Zmin = 99999
    prio_mini = 4
    suppr = 0
    prio = []
    data_tri = []
    pos = []
    ang = []
    face = []

    # Je les ai inversé c'est mieux (Youri)
    dic_ang = {
        (20, 25, 70): 90,
        (25, 20, 70): 0,
        (20, 70, 25): 90,
        (70, 20, 25): 0,
        (25, 70, 20): 90,
        (70, 25, 20): 0
    }

    dic_face = {
        70: 'small_face',
        25: 'medium_face',
        20: 'big_face'
    }

    for i in range(len(kapla_list)):
        if kapla_list[i]["attitude"][2] == 20:
            prio.append(0)
        elif kapla_list[i]["attitude"][2] == 25:
            prio.append(1)
        elif kapla_list[i]["attitude"][2] == 70:
            prio.append(2)

    for i in range(list_size):
        for y in range(len(kapla_list)):
            if Zmin > kapla_list[y]["base"][2]:
                Zmin = kapla_list[y]["base"][2]
        for y in range(len(kapla_list)):
            if kapla_list[y]["base"][2] == Zmin and prio_mini > prio[y]:
                prio_mini = prio[y]
                suppr = y
        Zmin = 99999
        prio_mini = 4
        data_tri.append(kapla_list[suppr])
        del kapla_list[suppr]

    for i in range(len(data_tri)):
        # Angle
        angle = dic_ang[tuple(data_tri[i]['attitude'])] + data_tri[i]['pivot']
        angle = angle % 180
        ang.append(angle)

        # Position
        pos_z = (data_tri[i]["base"][2] + (data_tri[i]["attitude"][2]))

        pos_x, pos_y = robot_to_world(data_tri[i]['pivot'],
                                      data_tri[i]["base"][0], data_tri[i]["base"][1],
                                      data_tri[i]["attitude"][0] / 2, data_tri[i]["attitude"][1] / 2)

        pos.append((pos_x, pos_y, pos_z))

        face.append(dic_face[data_tri[i]["attitude"][2]])

    for i in range(len(data)):
        yield pos[i], ang[i], face[i]


import math
import numpy as np


# Om = R * Or + Pr
def robot_to_world(robot_in_world_angle, robot_in_world_x, robot_in_world_y, object_in_robot_x, object_in_robot_y):  # Angle en degré
    alpha = math.radians(robot_in_world_angle)  # Conversion en rad
    pos_robot_in_world = np.array([robot_in_world_x, robot_in_world_y])  # Position Robot dans le repère Monde
    pos_object_in_robot = np.array([object_in_robot_x, object_in_robot_y])  # Position objet dans le repère Robot
    R = np.array([[math.cos(alpha), math.sin(-alpha)], [math.sin(alpha), math.cos(alpha)]])
    return R @ pos_object_in_robot + pos_robot_in_world
