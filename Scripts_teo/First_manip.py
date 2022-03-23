from serial.tools import list_ports
from pydobot import Dobot
import pydobot
import time as t
import sys
import math
import struct
from Change_targets import *


# -----------------------------------------------Function Part-----------------------------------------------#
def home_position(device):
    print('- home position (le robot recale et définit sa position zéro) ... ', end='')
    sys.stdout.flush()
    device.set_home(250.0, 0.0, 100.0)
    device.wait_for_cmd(device.home())
    print('[ok]')


def connection():
    print('- connexion au robot ...', end='')
    sys.stdout.flush()
    port = 'COM4'  # replacez ici COM3 par votre port de communication
    device = Dobot(port=port)
    print('[ok]')
    sys.stdout.flush()
    return device


def end_prog(device):
    print('- deconnexion')
    device.close()


def list_port():
    print('- liste des ports COM:')
    ports = list(list_ports.comports())
    for p in ports:
        print(p)


# -----------------------------------------------Get Position-----------------------------------------------#
def pretty_print_pose(pose):
    print('(x=%0.2f, y=%0.2f, z=%0.2f r=%0.2f)' % \
          (pose.position.x, pose.position.y, pose.position.z, pose.position.r))


def useful_print_position(position):
    print('(%0.2f, %0.2f, %0.2f, %0.2f)' % \
          (position.x, position.y, position.z, position.r))


def robot_position(device):
    print('- position du robot: ', end='')
    pose = device.get_pose()
    position = pose.position
    return position


def setup_position(connect):
    result = ""
    while result.lower() != "q":
        result = input("Appuyer sur ENTER pour afficher la postion actuelle, q pour quitter\n")
        useful_print_position(robot_position(connect))


# -----------------------------------------------Action Part-----------------------------------------------#
def move_x(a, device):
    position = robot_position(device)
    print('- mouvement en X ... ', end='')
    sys.stdout.flush()
    device.wait_for_cmd(device.move_to(position.x + a, position.y, position.z, position.r))
    print('[ok]')


def move_y(a, device):
    position = robot_position(device)
    print('- mouvement en Y ... ', end='')
    sys.stdout.flush()
    device.wait_for_cmd(device.move_to(position.x, position.y + a, position.z, position.r))
    print('[ok]')


def move_z(a, device):
    position = robot_position(device)
    print('- mouvement en Z ... ', end='')
    sys.stdout.flush()
    device.wait_for_cmd(device.move_to(position.x, position.y, position.z + a, position.r))
    print('[ok]')


def Rotation(a, device):
    position = robot_position(device)
    print('- mouvement en R ... ', end='')
    sys.stdout.flush()
    device.wait_for_cmd(device.move_to(position.x, position.y, position.z, position.r + a))
    print('[ok]')


def catch(device):
    print('- catch object ... ', end='')
    device.suck(True)
    print('[ok]')


def drop(device):
    print('- drop object ... ', end='')
    device.suck(False)
    print('[ok]')


def x_rotation(connect, rota, tempo):  # rota =100 pour 90°
    catch(connect)
    Rotation(rota, connect)
    t.sleep(tempo)
    Rotation(-rota, connect)
    drop(connect)
    t.sleep(tempo)


def move_to(device, x, y, z, r):
    print('- mouvement vertical rectiligne ... ', end='')
    device.wait_for_cmd(device.move_to(x, y, z, r, mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print('[ok]')


# -----------------------------------------------Conveyor Code-----------------------------------------------#

# -----------------------------------------------Running Code-----------------------------------------------#
# --------------Variable--------------#
val = 50  # move value
tempo = 2  # tempo en sec
tempo2 = 1
tempo_conveyor = 5
init_rota = 0
rota = 90  # 90° rotation

# --------------Init--------------#
device = connection()
device.set_home(250.0, 0.0, 100.0)
device.wait_for_cmd(device.home())

setup_position(device)
"""home_position(connect)
Rotation(init_rota,connect)

#--------------Action--------------#
move_to(connect,307,4,51,100)
catch(connect)
move_to(connect,180,173,-3,145)
drop(connect)


t.sleep(tempo2)
move_to(connect,180,173,5,145)
connect.conveyor_belt_distance(100,500, -1, 0)
t.sleep(tempo_conveyor)
connect.conveyor_belt_distance(100,500, 1, 0)
t.sleep(tempo2)
move_to(connect,172,-180,-1,55)

end_prog(connect)

#--------------Try--------------#
move_x(val,connect)
t.sleep(tempo)
move_x(-val,connect)
t.sleep(tempo)

move_y(val,connect)
t.sleep(tempo)
move_y(-val,connect)
t.sleep(tempo)

move_z(val,connect)
t.sleep(tempo)
move_z(-val,connect)
t.sleep(tempo)

x_rotation(connect,rota,tempo) 

connect.conveyor_belt_distance(100,500, 1, 0)

move_to(connect,150,0,40,0)
move_to(connect,150,0,100,0)

end_porg(connect)"""
