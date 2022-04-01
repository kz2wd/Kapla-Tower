from serial.tools import list_ports
from pydobot import Dobot
import pydobot
import time as t
import sys
import math
import struct
from dobot_extensions import Dobot
from First_manip import *

robot = connection()
result = ""

while result.lower() != "q":
    result = input("Appuyer sur ENTER pour afficher la postion actuelle, q pour quitter")
    robot_position(robot)
